import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.orm import Session
from ..services.game_connection_service import GameConnectionService
from .message_handlers import handle_manager_message, handle_player_message
from ..database import get_db


router = APIRouter()

game_connection_service = GameConnectionService()

@router.websocket("/ws/player/{room_code}")
async def websocket_player_endpoint(websocket: WebSocket, room_code: str, nickname: str, db: Session = Depends(get_db)):
    try:
        await game_connection_service.connect_player(websocket, room_code, nickname, db)
        
        while True:
            try:
                data = await websocket.receive_json()
                await handle_player_message(data, room_code, websocket)
                
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
                
            except Exception as e:
                #TODO: change to message
                await websocket.send_json({
                    "status": "error",
                    "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "error": "MESSAGE_PROCESSING_ERROR",
                    "detail": str(e)
                })

    except WebSocketDisconnect:
        game_connection_service.disconnect_player(websocket, room_code)
        
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason=str(e))
        game_connection_service.disconnect_player(websocket, room_code)
        raise
    
@router.websocket("/ws/manager")
async def websocket_manager_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
        
    try:
        room_code = game_connection_service.get_new_room_code()
        game_connection_service.create_room(room_code, websocket, db)
    except Exception as e:
        await websocket.close(code=4500, reason=str(e))
        return
        
    try:
        while True:
            data = await websocket.receive_json()
            await handle_manager_message(data, room_code, websocket)
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
