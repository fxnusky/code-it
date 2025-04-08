from typing import Dict, Optional, Set
from fastapi import WebSocket, Depends, HTTPException, status
import random
from sqlalchemy.orm import Session
from ..repositories.player_repository import PlayerRepository
from ..database import get_db
from ..repositories.room_repository import RoomRepository
from ..repositories.game_template_repository import GameTemplateRepository

class GameConnectionService:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, Optional[WebSocket] | Set[WebSocket]]] = {}
        self.status: str = "room_opened"
        self.current_question_id: str = None 
    
    def set_room_manager(self, room_code: str, manager: WebSocket):
        try: 
            if room_code not in self.rooms:
                self.rooms[room_code] = {"manager": manager, "players": set()}
            else:
                self.rooms[room_code]["manager"] = manager
        except HTTPException:
            raise
    
    def delete_room(self, room_code: str, db: Session):
        try: 
            room_repository = RoomRepository(db)
            room_repository.delete_room_by_code(room_code)
            if room_code in self.rooms:
                del self.rooms[room_code]
        except HTTPException:
            raise

    async def connect_player(self, websocket: WebSocket, room_code: str, nickname: str, db: Session):
        await websocket.accept()
        player_repository = PlayerRepository(db)
        room_repository = RoomRepository(db)

        room = room_repository.get_room_by_code(room_code)

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with code {room_code} not found"
            )
        
        try:
            player = player_repository.create_player(
                nickname=nickname,
                room_code=room_code
            )
            
            self.rooms[room_code]["players"].add(websocket)
            
            return {
                "status": "success",
                "player_id": player.id,
                "nickname": nickname,
                "room_code": room.room_code
            }

        except HTTPException as he:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise he
            
        except Exception as e:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "error": f"Connection failed: {str(e)}"
                }
            )

    async def disconnect_player(self, websocket: WebSocket, room_code: str):
        if room_code in self.rooms:
            self.rooms[room_code]["players"].discard(websocket)
        await websocket.close()

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_manager_message(self, message: dict, room_code: str):
        await self.rooms[room_code]["manager"].send_json(message)

    async def broadcast_players(self, content: dict, room_code: str):
        for connection in self.rooms[room_code]["players"]:
            await connection.send_json(content)