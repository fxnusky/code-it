from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.player_repository import PlayerRepository
from ..database import get_db
from ..schemas import PlayerCreate

router = APIRouter()

@router.get("/players")
def get_players(room_code: str, db: Session = Depends(get_db)):
    try:
        if not room_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room code is required"
            )
            
        player_repository = PlayerRepository(db)
        players = player_repository.get_players_by_room_code(room_code)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": players,
            "detail": "Players retrieved successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
