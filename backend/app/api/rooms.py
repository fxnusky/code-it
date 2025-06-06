from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.room_repository import RoomRepository
from ..services.room_service import RoomService
from ..database import get_db
from pydantic import BaseModel
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..repositories.game_template_repository import GameTemplateRepository
from typing import Optional


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
    
class RoomRequest(BaseModel):
    token: str
    template_id: int
    room_code: Optional[str] = None
    override: bool = False

@router.post("/rooms")
def create_room(request: RoomRequest, db: Session = Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        auth_service = AuthService(user_repository)
        if request.token[:5] != "load-":
            user = auth_service.get_or_create_user(request.token)
        else:
            user = auth_service.get_or_create_user_wo_token(request.token)
        if not request.override and user.active_room:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail={
                    "status": "error",
                    "status_code": status.HTTP_405_METHOD_NOT_ALLOWED,
                    "detail": "This user has already a game in progress.",
                    "data": {"room_code": user.active_room}
                }
            ) 
        template_repository = GameTemplateRepository(db)
        template = template_repository.get_template_by_id(request.template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "error",
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "detail": f"The template with ID {request.template_id} does not exist.",
                    "data": None
                }
            ) 
        room_repository = RoomRepository(db)
        room_service = RoomService(room_repository)
        room_code = request.room_code
        if not room_code:
            room_code = room_service.get_room_code()
        room_service.create_room(room_code, request.template_id)
        auth_service.update_active_room(user.google_id, room_code)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": {"room_code": room_code},
            "detail": "Room created successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )