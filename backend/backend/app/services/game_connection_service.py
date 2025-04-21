from typing import Dict, Optional, Set
from fastapi import WebSocket,  HTTPException
from sqlalchemy.orm import Session
from ..repositories.room_repository import RoomRepository
class GameConnectionService:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, Optional[WebSocket] | Dict[str, WebSocket]]] = {}
        self.state: str = "room_opened"
        self.current_question_id: str = None 
    
    def set_room_manager(self, room_code: str, manager: WebSocket):
        try: 
            if room_code not in self.rooms:
                self.rooms[room_code] = {"manager": manager, "players": {}}
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

    async def connect_player(self, websocket: WebSocket, room_code: str, player_id: int):
        await websocket.accept()
        self.rooms[room_code]["players"][player_id] = websocket

    async def disconnect_player(self, websocket: WebSocket, room_code: str, player_id: int):
        if room_code in self.rooms and player_id in self.rooms[room_code]["players"]:
            del self.rooms[room_code]["players"][player_id]
        await websocket.close()

    async def disconnect_manager(self, room_code: str):
        if room_code in self.rooms:
            await self.rooms[room_code]["manager"].close()
            self.rooms[room_code]["manager"] = None

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_manager_message(self, message: dict, room_code: str):
        await self.rooms[room_code]["manager"].send_json(message)

    async def broadcast_players(self, content: dict, room_code: str):
        for connection in self.rooms[room_code]["players"].values():
            await connection.send_json(content)

    async def set_state(self, new_state: str, room_code: str, db: Session):
        try: 
           if self.state != new_state:
            room_repository = RoomRepository(db)
            room_repository.update_room_state(new_state, room_code)
            self.state = new_state
        except HTTPException:
            raise
        