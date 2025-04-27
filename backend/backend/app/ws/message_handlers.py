from fastapi import WebSocket
from ..services.game_connection_service import GameConnectionService
from ..services.question_service import QuestionService
from ..services.submission_service import SubmissionService
from ..services.test_case_execution_service import TestCaseExecutionService
import logging
from sqlalchemy.orm import Session
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def handle_manager_message(data: dict, room_code: str, game_connection_service: GameConnectionService, db: Session, question_service: QuestionService, submission_service: SubmissionService, test_case_execution_service: TestCaseExecutionService):
    logger.info(f"Received manager message: {data}")
    if data["action"] == "start_game" or  data["action"] == "next_question":
        question_id = data["question_id"]
        game_connection_service.current_question_id = question_id
        question = question_service.get_question_by_id(question_id)
        await game_connection_service.set_state("question", room_code, db)
        await game_connection_service.send_manager_message({"action": "question", "question": question}, room_code)
        await game_connection_service.broadcast_players({"action": "question", "question": question}, room_code)
        game_connection_service.current_question_time = question["time_limit"]
        game_connection_service.current_question_timestamp = datetime.now()

    elif data["action"] == "end_question":
        await game_connection_service.set_state("question_results", room_code, db)
        question_id = data["question_id"]
        result_stats = submission_service.get_question_results_stats(room_code, question_id)
        await game_connection_service.send_manager_message({"action": "question_results", "stats": result_stats}, room_code)
        for player_id, connection in game_connection_service.rooms[room_code]["players"].items():
            points = submission_service.get_question_results_by_player(player_id, data["question_id"])
            test_case_executions = test_case_execution_service.get_question_results_by_player(player_id, data["question_id"])
            question_results = {
                "total_points": points["total_points"],
                "question_points": points["question_points"],
                "test_case_executions": test_case_executions
            }
            await game_connection_service.send_message({"action": "question_results", "question_results": question_results}, connection)
    elif data["action"] == "show_ranking":
        players_points = submission_service.get_total_points_players(room_code)
        await game_connection_service.set_state("ranking", room_code, db)
        await game_connection_service.send_manager_message({"action": "ranking", "ranking": players_points}, room_code)
        for player_id, info in players_points.items():
            await game_connection_service.send_message({"action": "ranking", "points": info["total_points"], "position": info["position"]}, game_connection_service.rooms[room_code]["players"][player_id])
    elif data["action"] == "end_game":
        players_points = submission_service.get_total_points_players(room_code)
        await game_connection_service.set_state("game_ended", room_code, db)
        await game_connection_service.send_manager_message({"action": "ranking", "ranking": players_points}, room_code)
        for player_id, info in players_points.items():
            await game_connection_service.send_message({"action": "game_ended", "points": info["total_points"], "position": info["position"]}, game_connection_service.rooms[room_code]["players"][player_id])        

    else:
        logger.info(f"Unknown message from manager {data}")
    

async def handle_player_message(data: dict, room_code: str, websocket: WebSocket, game_connection_service: GameConnectionService, submission_service: SubmissionService):
    logger.info(f"Received player message: {data}")
    if data["action"] == "submit_question":
        coding_time = int((datetime.now() - game_connection_service.current_question_timestamp).total_seconds())
        time = game_connection_service.current_question_time
        if time == 0:
            time = 1
        factor = (2-(coding_time/game_connection_service.current_question_time))/2
        submission_id = data["submission_id"]
        submission = submission_service.get_submissions_by_submission_id(submission_id)
        
        points = 0
        if submission:
            points = submission.earned_points * factor
        
        submission_service.update_submission_points(submission_id, points)
        await game_connection_service.send_message({"action": "question_submitted"}, websocket)
        await game_connection_service.send_manager_message({"action": "player_submitted"}, room_code)
    else:
        logger.info(f"Unknown message from manager {data}")