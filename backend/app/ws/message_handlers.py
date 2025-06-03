from fastapi import WebSocket
from ..services.game_connection_service import GameConnectionService
from ..services.question_service import QuestionService
from ..services.auth_service import AuthService
from ..services.submission_service import SubmissionService
from ..services.test_case_execution_service import TestCaseExecutionService
from ..repositories.user_repository import UserRepository
import logging
from sqlalchemy.orm import Session
from datetime import datetime
import time
import asyncio
from fastapi.websockets import WebSocketState

def current_milli_time():
    return int(time.time_ns() / 1_000_000)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def handle_manager_message(data: dict, room_code: str, game_connection_service: GameConnectionService, db: Session, question_service: QuestionService, submission_service: SubmissionService, test_case_execution_service: TestCaseExecutionService, user_repository: UserRepository, token: str, auth_service: AuthService):
    t1 = current_milli_time()
    logger.info(f"Received manager message: {data}")
    if data["action"] == "start_game" or  data["action"] == "next_question":
        question_id = data["question_id"]
        game_connection_service.set_current_question_id(room_code, question_id)
        question = question_service.get_question_by_id(question_id)
        await game_connection_service.set_state("question", room_code, db)
        await game_connection_service.send_manager_message({"action": "question", "question": question}, room_code)
        await game_connection_service.broadcast_players({"action": "question", "question": question}, room_code, t1)
        game_connection_service.set_current_question_time(room_code, question["time_limit"])
        game_connection_service.set_current_question_timestamp(room_code, datetime.now())

    elif data["action"] == "end_question":
        await game_connection_service.set_state("question_results", room_code, db)
        question_id = data["question_id"]
        result_stats = submission_service.get_question_results_stats(room_code, question_id)
        await game_connection_service.send_manager_message({"action": "question_results", "stats": result_stats}, room_code)
        for player_id, connection in game_connection_service.rooms[room_code]["players"].items():
            if connection.client_state != WebSocketState.DISCONNECTED:
                points = submission_service.get_question_results_by_player(player_id, data["question_id"])
                test_case_executions = test_case_execution_service.get_question_results_by_player(player_id, data["question_id"])
                question_results = {
                    "total_points": points["total_points"],
                    "question_points": points["question_points"],
                    "test_case_executions": test_case_executions
                }
                t2 = current_milli_time()
                await game_connection_service.send_message({"action": "question_results", "question_results": question_results, "X-Req-Insights": f"received={t1},sent={t2}"}, connection)
    elif data["action"] == "show_ranking":
        players_points = submission_service.get_total_points_players(room_code)
        await game_connection_service.set_state("ranking", room_code, db)
        await game_connection_service.send_manager_message({"action": "ranking", "ranking": players_points}, room_code)
        for player_id, info in players_points.items():
            t2 = current_milli_time()
            ws = game_connection_service.rooms[room_code]["players"].get(player_id, None)
            if ws and ws.client_state != WebSocketState.DISCONNECTED:
                await game_connection_service.send_message({"action": "ranking", "points": info["total_points"], "position": info["position"], "X-Req-Insights": f"received={t1},sent={t2}"}, ws)
    elif data["action"] == "end_game":
        try:
            players_points = submission_service.get_total_points_players(room_code)
            await game_connection_service.set_state("game_ended", room_code, db)
            
            # Send final messages first
            await game_connection_service.send_manager_message(
                {"action": "ranking", "ranking": players_points}, 
                room_code
            )
            
            # Disconnect all players
            disconnect_tasks = []
            if room_code in game_connection_service.rooms:
                for player_id, info in players_points.items():
                    try:
                        player_ws = game_connection_service.rooms[room_code]["players"].get(player_id)
                        if player_ws and player_ws.client_state != WebSocketState.DISCONNECTED:
                            t2 = current_milli_time()
                            await player_ws.send_json({
                                "action": "game_ended",
                                "points": info["total_points"],
                                "position": info["position"],
                                "X-Req-Insights": f"received={t1},sent={t2}"
                            })
                            
                            disconnect_tasks.append(
                                game_connection_service.disconnect_player(
                                    player_ws,
                                    room_code,
                                    player_id
                                )
                            )
                    except Exception as e:
                        logger.error(f"Error handling player {player_id}: {str(e)}")
                
                # Execute all disconnects
                if disconnect_tasks:
                    await asyncio.gather(*disconnect_tasks, return_exceptions=True)
                
                # Update active room and disconnect manager
                try:
                    user = auth_service.get_or_create_user(token)
                    user_repository.update_active_room(user.google_id, "")
                except Exception as e:
                    logger.error(f"Failed to update active room: {str(e)}")
                
                # Disconnect manager and clean up
                await game_connection_service.disconnect_manager(room_code)
                game_connection_service.delete_room(room_code, db)
                
        except Exception as e:
            logger.error(f"Error during game end: {str(e)}")
            # Force cleanup if something went wrong
            if room_code in game_connection_service.rooms:
                game_connection_service.delete_room(room_code, db)
            

    else:
        logger.info(f"Unknown message from manager {data}")
    

async def handle_player_message(data: dict, room_code: str, websocket: WebSocket, game_connection_service: GameConnectionService, submission_service: SubmissionService):
    logger.info(f"Received player message: {data}")
    if data["action"] == "submit_question":
        coding_time = int((datetime.now() - game_connection_service.get_current_question_timestamp(room_code)).total_seconds())
        time = game_connection_service.get_current_question_time(room_code)
        if time == 0:
            time = 1
        factor = (2-(coding_time/game_connection_service.get_current_question_time(room_code)))/2
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