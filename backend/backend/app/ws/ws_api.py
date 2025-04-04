import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, Query
from sqlalchemy.orm import Session
from ..services.game_connection_service import GameConnectionService
from .message_handlers import handle_manager_message, handle_player_message
from ..database import get_db
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository


router = APIRouter()

game_connection_service = GameConnectionService()

@router.websocket("/ws/player/{room_code}")
async def websocket_player_endpoint(websocket: WebSocket, room_code: str, nickname: str, db: Session = Depends(get_db)):
    try:
        response = await game_connection_service.connect_player(websocket, room_code, nickname, db)
        if (response["status"] =="success"):
            await game_connection_service.send_message({"action": "joined"}, websocket)
            await game_connection_service.send_manager_message({"action": "player_joined"}, room_code)
       
        while True:
            try:
                data = await websocket.receive_json()
                await handle_player_message(data, room_code, websocket, game_connection_service)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                #TODO: change to message
                await websocket.send_json({
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": "INVALID_JSON",
                    "detail": "Invalid JSON format"
                })
                break
            except Exception as e:
                #TODO: change to message
                await websocket.send_json({
                    "status": "error",
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "error": "MESSAGE_PROCESSING_ERROR",
                    "detail": str(e)
                })
                break

    except WebSocketDisconnect:
        await game_connection_service.disconnect_player(websocket, room_code)
        
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason=str(e))
        await game_connection_service.disconnect_player(websocket, room_code)
        raise
    
@router.websocket("/ws/manager")
async def websocket_manager_endpoint(websocket: WebSocket, token: str = Query(...), db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        user_repository = UserRepository(db)
        auth_service = AuthService(user_repository)
        user = auth_service.get_or_create_user(token)
        if user.active_room:
            await websocket.close(
                code=4001,
                reason="User already has an active room"
            )
            return
        room_code = game_connection_service.get_new_room_code()
        auth_service.update_active_room(user.google_id, room_code)
        game_connection_service.create_room(room_code, websocket, db)
        await game_connection_service.send_message({"action": "room_opened", "room_code": room_code}, websocket)
    except Exception as e:
        await websocket.close(code=4500, reason=str(e))
        return
        
    try:
        while True:
            try:
                data = await websocket.receive_json()
                await handle_manager_message(data, room_code, game_connection_service)
            except WebSocketDisconnect:
                break
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
