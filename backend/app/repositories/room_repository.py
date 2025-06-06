from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Room
from fastapi import HTTPException, status

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_room(self, room_code: str, template_id: int):
        try:
            existing_room = self.get_room_by_code(room_code)
            if existing_room:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A room with '{room_code}' already exists"
                )
            room = Room(room_code=room_code, template_id=template_id, game_state="room_opened")
            self.db.add(room)
            self.db.commit()
            self.db.refresh(room)
            return room
        except HTTPException:
            raise
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

    def delete_room_by_code(self, room_code: int):
        try:
            room = self.db.query(Room).filter(Room.room_code == room_code).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with code {room_code} not found"
                )
                
            self.db.delete(room)
            self.db.commit()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving players"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting room: {str(e)}"
            )
    
    def get_room_by_code(self, room_code: str):
        try:
            return self.db.query(Room).filter(Room.room_code == room_code).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving players"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while retrieving players"
            )
    
    def get_rooms(self):
        try:
             return self.db.query(Room).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving players"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while retrieving players"
            )
    def get_existing_room_codes(self):
        try:
             return {code for (code,) in self.db.query(Room.room_code).all()}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving players"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while retrieving players"
            )
        
    def update_room_state(self, new_state: str, room_code: str):
        try:
            room = self.db.query(Room).filter(Room.room_code == room_code).first()
            
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Room not found"
                )
                
            room.game_state = new_state
            self.db.commit()
            self.db.refresh(room)
            return room
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while updating the room state"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while updating the room state"
            )
            

       
    
            