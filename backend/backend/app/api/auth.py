from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..database import get_db

router = APIRouter()

class TokenRequest(BaseModel):
    token: str

@router.post("/validate-token")
def validate_token(request: TokenRequest, db: Session = Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        auth_service = AuthService(user_repository)
        user = auth_service.get_or_create_user(request.token)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": {"user": user},
            "detail": "User registered successfully",
        } 
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        users = user_repository.get_users()
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": {"uses": users},
            "detail": "Users retrieved successfully",
        } 
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status="error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
