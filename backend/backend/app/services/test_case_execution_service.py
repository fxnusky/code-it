from app.repositories.test_case_execution_repository import TestCaseExecutionRepository
from fastapi import HTTPException

class TestCaseExecutionService:
    def __init__(self, test_case_execution_repository: TestCaseExecutionRepository):
        self.test_case_execution_repository = test_case_execution_repository

    def compute_earned_points(self, submission_id: int, num_test_cases: int):
        try:
            if num_test_cases:
                return self.test_case_execution_repository.get_correct_test_case_executions_by_submission_id(submission_id) * 1000/num_test_cases
            return 0
        except HTTPException:
            raise
    
    def create_test_case_execution(self, submission_id: int, case_id: int, obtained_output: str, correct: bool):
        try:
            return self.test_case_execution_repository.create_test_case_execution(submission_id, case_id, obtained_output, correct) 
        except HTTPException:
            raise
    