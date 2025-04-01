from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..database import get_db

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    users = user_repository.get_all_users()
    return users