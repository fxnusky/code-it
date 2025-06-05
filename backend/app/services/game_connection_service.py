from typing import Dict, Optional
from fastapi import WebSocket,  HTTPException
from sqlalchemy.orm import Session
from ..repositories.room_repository import RoomRepository
from datetime import datetime
import time
import logging
import asyncio
from fastapi.websockets import WebSocketState
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
class GameConnectionService:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, Optional[WebSocket] | Dict[str, WebSocket]]] = {}
    
    def set_room_manager(self, room_code: str, manager: WebSocket):
        try: 
            if room_code not in self.rooms:
                self.rooms[room_code] = {"manager": manager, "players": {}, "state": "room_opened", "current_question_id": None, "current_question_timestamp": None, "current_question_time": None}
            else:
                if self.rooms[room_code]["manager"] != None and self.rooms[room_code]["manager"].client_state != WebSocketState.DISCONNECTED:
                    self.rooms[room_code]["manager"].close()
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
        if self.rooms.get(room_code):
            await websocket.accept()
            if self.rooms[room_code]["players"].get(player_id) and self.rooms[room_code]["players"][player_id].client_state != WebSocketState.DISCONNECTED:
                self.rooms[room_code]["players"][player_id].close()
            self.rooms[room_code]["players"][player_id] = websocket

    async def disconnect_player(self, websocket: WebSocket, room_code: str, player_id: int):
        logger.info(f"Disconnecting player: {player_id}")
        try:
            if (room_code in self.rooms and 
                player_id in self.rooms[room_code]["players"] and
                websocket.client_state != WebSocketState.DISCONNECTED):
                
                await websocket.close()
                del self.rooms[room_code]["players"][player_id]
        except Exception as e:
            logger.error(f"Error disconnecting player {player_id}: {str(e)}")

    async def disconnect_manager(self, room_code: str):
        logger.info(f"Disconnecting manager: {room_code}")
        try:
            if (room_code in self.rooms and 
                self.rooms[room_code]["manager"] and 
                self.rooms[room_code]["manager"].client_state != WebSocketState.DISCONNECTED):
                
                await self.rooms[room_code]["manager"].close()
                self.rooms[room_code]["manager"] = None
        except Exception as e:
            logger.error(f"Error disconnecting manager: {str(e)}")

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_manager_message(self, message: dict, room_code: str):
        if self.rooms[room_code] and self.rooms[room_code]["manager"] and self.rooms[room_code]["manager"].client_state != WebSocketState.DISCONNECTED:
            await self.rooms[room_code]["manager"].send_json(message)

    async def broadcast_players(self, content: dict, room_code: str, t1:str =-1):
        if self.rooms[room_code]:
            tasks = []
            t2 = self.current_milli_time()
            content["X-Req-Insights"] = f"received={t1},sent={t2}"
            for connection in self.rooms[room_code]["players"].values():
                if connection.client_state != WebSocketState.DISCONNECTED:
                    tasks.append(connection.send_json(content))
            await asyncio.gather(*tasks)

    async def set_state(self, new_state: str, room_code: str, db: Session):
        try: 
           if self.rooms.get(room_code) and self.rooms[room_code]["state"] != new_state:
            room_repository = RoomRepository(db)
            room_repository.update_room_state(new_state, room_code)
            self.rooms[room_code]["state"] = new_state
        except HTTPException:
            raise
    def get_state(self, room_code: str):
        if self.rooms.get(room_code):
            return self.rooms[room_code]["state"]
    def get_current_question_id(self, room_code: str):
        if self.rooms.get(room_code):
            return self.rooms[room_code]["current_question_id"]
    def set_current_question_id(self, room_code: str, new_question_id: int):
        if self.rooms.get(room_code):
            self.rooms[room_code]["current_question_id"] = new_question_id

    def get_current_question_timestamp(self, room_code: str):
        if self.rooms.get(room_code):
            return self.rooms[room_code]["current_question_timestamp"]
    def set_current_question_timestamp(self, room_code: str, new_question_timestamp: int):
        if self.rooms.get(room_code):
            self.rooms[room_code]["current_question_timestamp"] = new_question_timestamp

    def get_current_question_time(self, room_code: str):
        if self.rooms.get(room_code):
            return self.rooms[room_code]["current_question_time"]
    def set_current_question_time(self, room_code: str, new_question_time: int):
        if self.rooms.get(room_code):
            self.rooms[room_code]["current_question_time"] = new_question_time

    def current_milli_time(self):
        return int(time.time_ns() / 1_000_000)

        