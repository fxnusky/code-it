from sqlalchemy.orm import Session
from app.models import Question, Room
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
    def get_question_ids_by_room_code(self, room_code: str):
        try:
            return self.db.query(Question.id, Question.order_key)\
                   .join(Room, Question.template_id == Room.template_id)\
                   .filter(Room.room_code == room_code)\
                   .order_by(Question.order_key)\
                   .all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving question ids"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    