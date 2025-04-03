from fastapi import WebSocket
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def handle_manager_message(data: dict, room_code: str, websocket: WebSocket):
    logger.info(f"Received manager message: {data}")

async def handle_player_message(data: dict, room_code: str, websocket: WebSocket):
    logger.info(f"Received player message: {data}")