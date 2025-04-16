from sqlalchemy.orm import Session
from app.models import TestCaseExecution
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class TestCaseExecutionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_correct_test_case_executions_by_submission_id(self, submission_id: int):
        try:
            return self.db.query(TestCaseExecution).filter(TestCaseExecution.submission_id == submission_id, TestCaseExecution.correct == True).count()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving submission"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    def create_test_case_execution(self, submission_id: int, case_id: int, obtained_output: str, correct: bool):
        try:
            test_case_execution = TestCaseExecution(submission_id=submission_id, case_id=case_id, obtained_output=obtained_output, correct=correct)
            self.db.add(test_case_execution)
            self.db.commit()
            self.db.refresh(test_case_execution)
            return test_case_execution
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while creating test case execution"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )