from fastapi import WebSocket
from ..services.game_connection_service import GameConnectionService
from ..services.question_service import QuestionService
from ..services.submission_service import SubmissionService
from ..services.test_case_execution_service import TestCaseExecutionService
import logging
from sqlalchemy.orm import Session


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
        # Get ranking and send it
        await game_connection_service.set_state("ranking", room_code, db)
        await game_connection_service.send_manager_message({"action": "ranking"}, room_code)
        await game_connection_service.broadcast_players({"action": "ranking"}, room_code)
    elif data["action"] == "end_game":
        # Get ranking and send it
        await game_connection_service.set_state("game_ended", room_code, db)
        await game_connection_service.send_manager_message({"action": "ranking"}, room_code)
        await game_connection_service.broadcast_players({"action": "game_ended"}, room_code)

    else:
        logger.info(f"Unknown message from manager {data}")
    

async def handle_player_message(data: dict, room_code: str, websocket: WebSocket, game_connection_service: GameConnectionService):
    logger.info(f"Received player message: {data}")
    if data["action"] == "submit_question":
        # submit question and if correct send this message:
        await game_connection_service.send_message({"action": "question_submitted"}, websocket)
        await game_connection_service.send_manager_message({"action": "player_submitted"}, room_code)
    else:
        logger.info(f"Unknown message from manager {data}")