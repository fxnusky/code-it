from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.player_repository import PlayerRepository
from ..repositories.room_repository import RoomRepository
from ..services.room_service import RoomService
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@router.get("/player/{token}")
def get_players(token: str, db: Session = Depends(get_db)):
    try:  
        player_repository = PlayerRepository(db)
        player = player_repository.get_player_by_token(token)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": player,
            "detail": "Player retrieved successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )    
@router.post("/players", status_code=status.HTTP_201_CREATED)
def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db)
):
    try:
        player_repository = PlayerRepository(db)
        room_repository = RoomRepository(db)
        room_service = RoomService(room_repository)
        room_state = room_service.get_room_state(player_data.room_code)
        if room_state != "room_opened":
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="The game is already in progress"
            )
        num_players = len(player_repository.get_players_by_room_code(player_data.room_code))
        # HARDCODED NUMBER
        if num_players >= 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The room is already full"
            )
        player = player_repository.create_player(
            nickname=player_data.nickname,
            room_code=player_data.room_code
        )
        
        return {
            "status": "success",
            "data": player
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "error": str(e)
            }
        )