from sqlalchemy.orm import Session
from app.models import TestCase
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class TestCaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_test_cases_by_question_id(self, question_id: int):
        try:
            return self.db.query(TestCase).filter(TestCase.question_id == question_id).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving test cases"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )