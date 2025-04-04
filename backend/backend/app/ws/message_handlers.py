from fastapi import WebSocket
from ..services.game_connection_service import GameConnectionService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def handle_manager_message(data: dict, room_code: str, game_connection_service: GameConnectionService):
    logger.info(f"Received manager message: {data}")
    if data.action == "start_game" or  data.action == "next_question":
        # Recieve question id
        # Get question content and send it
        game_connection_service.send_manager_message({"action": "question"}, room_code)
        game_connection_service.broadcast_players({"action": "question"})
    elif data.action == "end_question":
        # Recieve question id
        # Get question results and send it
        game_connection_service.send_manager_message({"action": "question_results"}, room_code)
        game_connection_service.broadcast_players({"action": "question_results"})
    elif data.action == "show_ranking":
        # Get ranking and send it
        game_connection_service.send_manager_message({"action": "ranking"}, room_code)
        game_connection_service.broadcast_players({"action": "ranking"})
    elif data.action == "end_game":
        # Get ranking and send it
        game_connection_service.send_manager_message({"action": "ranking"}, room_code)
        game_connection_service.broadcast_players({"action": "game_ended"})

    else:
        logger.info(f"Unknown message from manager {data}")
    

async def handle_player_message(data: dict, room_code: str, websocket: WebSocket, game_connection_service: GameConnectionService):
    logger.info(f"Received player message: {data}")
    if data.action == "submit_question":
        # submit question and if correct send this message:
        game_connection_service.send_message({"action": "question_submitted"}, websocket)
        game_connection_service.send_manager_message({"action": "player_submitted"}, room_code)
    else:
        logger.info(f"Unknown message from manager {data}")