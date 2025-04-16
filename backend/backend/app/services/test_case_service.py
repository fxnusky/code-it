from app.repositories.test_case_repository import TestCaseRepository
from fastapi import HTTPException

class TestCaseService:
    def __init__(self, test_case_repository: TestCaseRepository):
        self.test_case_repository = test_case_repository

    def get_test_cases_by_question_id(self, question_id: int):
        try:
            return self.test_case_repository.get_test_cases_by_question_id(question_id)
        except HTTPException:
            raise
        