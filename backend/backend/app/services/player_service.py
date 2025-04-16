from app.repositories.player_repository import PlayerRepository
from fastapi import HTTPException

class PlayerService:
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository

    def get_players_by_room_code(self, room_code: str):
        try:
            players = self.player_repository.get_players_by_room_code(room_code)
            return [{"id": player.id, "nickname": player.nickname} for player in players]
        except HTTPException:
            raise
    
    def verify_token(self, token: str, room_code:str):
        try:
            player = self.player_repository.get_player_by_token(token)
            if player and player.room_code == room_code:
                return True
            return False
        except HTTPException:
            raise
    def get_player_id_by_token(self, token: str):
        try:
            player = self.player_repository.get_player_by_token(token)
            return player.id
        except HTTPException:
            raise