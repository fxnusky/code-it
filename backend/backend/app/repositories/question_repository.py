from sqlalchemy.orm import Session
from app.models import Question
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_question_by_id(self, question_id: int):
        try:
            return self.db.query(Question).filter(Question.id == question_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving question"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    def get_question_ids_by_template_id(self, template_id: int):
        try:
            return self.db.query(Question.id, Question.order_key).filter(Question.template_id == template_id).order_by(Question.order_key.asc()).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving question"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    