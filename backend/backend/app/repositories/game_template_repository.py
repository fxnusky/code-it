from sqlalchemy.orm import Session
from app.models import GameTemplate
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class GameTemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_template_by_id(self, template_id: int):
        try:
            return self.db.query(GameTemplate).filter(GameTemplate.id == template_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving user"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    