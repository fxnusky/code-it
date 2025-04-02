from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Player
from fastapi import HTTPException, status

class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_player(self, nickname: str, room_code: str):
        existing_player = self.get_player_by_nickname_and_room(nickname, room_code)
        
        if existing_player:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Player with nickname '{nickname}' already exists in room '{room_code}'"
            )

        try:
            player = Player(room_code=room_code, nickname=nickname)
            self.db.add(player)
            self.db.commit()
            self.db.refresh(player)
            return player
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    def delete_player_by_id(self, player_id: int):
        try:
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Player with ID {player_id} not found"
                )
                
            self.db.delete(player)
            self.db.commit()
            return {"message": f"Player {player_id} deleted successfully"}
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting player: {str(e)}"
            )

    def get_players_by_room_code(self, room_code: str):
        try:
            return self.db.query(Player).filter(Player.room_code == room_code).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving players"
            )
        except Exception as e:
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while retrieving players"
            )
        
    def get_player_by_nickname_and_room(self, nickname: str, room_code: str):
        return self.db.query(Player).filter(
            Player.nickname == nickname,
            Player.room_code == room_code
        ).first()