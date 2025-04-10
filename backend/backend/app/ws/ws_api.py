import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from ..services.game_connection_service import GameConnectionService
from .message_handlers import handle_manager_message, handle_player_message
from ..database import get_db
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..services.question_service import QuestionService
from ..repositories.question_repository import QuestionRepository
from ..services.player_service import PlayerService
from ..repositories.player_repository import PlayerRepository
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


router = APIRouter()

game_connection_service = GameConnectionService()

@router.websocket("/ws/player")
async def websocket_player_endpoint(websocket: WebSocket, token: str = Query(...),  room_code: str = Query(...), nickname: str = Query(...), db: Session = Depends(get_db)):
    try:
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        valid_token = player_service.verify_token(token, room_code)
        if not valid_token:
            await websocket.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This player is not authorized to connect to this room."
            )
        await game_connection_service.connect_player(websocket, room_code)
        await game_connection_service.send_message({"action": "status", "state": "joined", "room_code": room_code, "nickname": nickname}, websocket)
        await game_connection_service.send_manager_message({"action": "player_joined"}, room_code)
       
        while True:
            try:
                data = await websocket.receive_json()
                await handle_player_message(data, room_code, websocket, game_connection_service)
                
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        await game_connection_service.disconnect_player(websocket, room_code)
        await game_connection_service.send_manager_message({"action": "player_disconnected"})
        
        
    except Exception as e:
        logger.error(str(e))
    
@router.websocket("/ws/manager")
async def websocket_manager_endpoint(websocket: WebSocket, token: str = Query(...),  room_code: str = Query(...), db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        user_repository = UserRepository(db)
        auth_service = AuthService(user_repository)
        user = auth_service.get_or_create_user(token)
        if not user.active_room == room_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This user is not authorized to manage this room."
            )
        game_connection_service.set_room_manager(user.active_room, websocket)
        
        question_repository = QuestionRepository(db)
        question_service = QuestionService(question_repository)
        question_ids = question_service.get_sorted_question_ids(room_code)
        
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        players = player_service.get_players_by_room_code(room_code)

        await game_connection_service.send_message({
            "action": "status", 
            "state": game_connection_service.state, 
            "question_ids": question_ids, 
            "players": players, 
            "current_question_id": game_connection_service.current_question_id
            }, websocket)
    except Exception as e:
        logger.error(str(e))
        
    try:
        while True:
            try:
                data = await websocket.receive_json()
                await handle_manager_message(data, room_code, game_connection_service, db)
            except WebSocketDisconnect:
                break
    except Exception as e:
        logger.error(str(e))
