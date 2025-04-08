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