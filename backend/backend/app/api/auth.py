from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..database import get_db

router = APIRouter()

class TokenRequest(BaseModel):
    token: str

@router.post("/api/validate-token")
def validate_token(request: TokenRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    user = auth_service.get_or_create_user(request.token) 
    return {"success": True, "user": user}
