from sqlalchemy.orm import Session 
from app.models import TestCaseExecution, Submission, TestCase, Question
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
            test_case_execution = (self.db.query(TestCaseExecution)
                .join(Submission, TestCaseExecution.submission_id == Submission.submission_id)
                .filter(
                    Submission.submission_id==submission_id, 
                    TestCaseExecution.case_id==case_id
                )
                .order_by(TestCaseExecution.case_id)
                .first())
            if not test_case_execution:
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
    
    def get_test_case_executions(self, player_id: int, question_id: int):
        try:
            test_case_executions =  (
                self.db.query(TestCaseExecution)
                .join(Submission, TestCaseExecution.submission_id == Submission.submission_id)
                .filter(
                    Submission.player_id == player_id,
                    Submission.question_id == question_id
                )
                .order_by(TestCaseExecution.case_id)
                .all()
            )
            if test_case_executions:
                return [{
                    "case_id": tce.case_id,
                    "correct": tce.correct
                } for tce in test_case_executions]
            else:
                test_cases =  (
                    self.db.query(TestCase)
                    .filter(
                        TestCase.question_id == question_id
                    )
                    .order_by(TestCase.case_id)
                    .all()
                )
                return [{
                    "case_id": tc.case_id,
                    "correct": False
                } for tc in test_cases]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the test case executions"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        