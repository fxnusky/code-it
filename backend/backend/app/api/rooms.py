from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.room_repository import RoomRepository
from ..database import get_db

router = APIRouter()

@router.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    try:
        room_repository = RoomRepository(db)
        rooms = room_repository.get_rooms()
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": rooms,
            "detail": "Rooms retrieved successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/rooms/{room_id}")
def delete_player(
    room_id: int,
    db: Session = Depends(get_db)
):
    room_repository = RoomRepository(db)
    
    try:
        room_repository.delete_room_by_id(room_id)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "detail": f"Player {room_id} deleted",
            "data": {
                "deleted_id": room_id
            }
            
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )