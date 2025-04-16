from app.repositories.submission_repository import SubmissionRepository
from fastapi import HTTPException

class SubmissionService:
    def __init__(self, submission_repository: SubmissionRepository):
        self.submission_repository = submission_repository

    def create_submission(self, question_id: int, player_id: int, code: str):
        try:
            submission = self.submission_repository.create_submission(question_id, player_id, code)
            return {
                    "id": submission.submission_id,
                }
        except HTTPException: 
            raise
    def update_submission_points(self, submission_id: int, new_points: int):
        try:
            self.submission_repository.update_submission_points(submission_id, new_points)
        except HTTPException: 
            raise
    
   

        