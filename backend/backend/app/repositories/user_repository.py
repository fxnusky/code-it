from sqlalchemy.orm import Session
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_google_id(self, google_id: str):
        try:
            return self.db.query(User).filter(User.google_id == google_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving user"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    def get_users(self):
        try:
            return self.db.query(User).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving user"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    def create_user(self, google_id: str, email: str, name: str):
        try:
            user = User(google_id=google_id, email=email, name=name)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            raise HTTPException(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving user"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )