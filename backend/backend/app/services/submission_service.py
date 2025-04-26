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
    
    def get_submissions_by_submission_id(self, submission_id: int):
        try:
            return self.submission_repository.get_submissions_by_submission_id(submission_id)
        except HTTPException: 
            raise

    def get_question_results_by_player(self, player_id: int, question_id: int):
        try:
            submission = self.submission_repository.get_submission(player_id, question_id)
            total_points = self.submission_repository.get_total_points_by_player_id(player_id)
            earned_points = 0
            if submission:
                earned_points = submission.earned_points
            return {
                    "total_points": total_points,
                    "question_points": earned_points
                }
        except HTTPException: 
            raise
    def get_question_results_stats(self, room_code: str, question_id: int):
        try:
            return self.submission_repository.get_question_results_stats(room_code, question_id)
        except HTTPException: 
            raise

    def get_submission_by_question_player(self, player_id: str, question_id: int):
        try:
            return self.submission_repository.get_submission(player_id, question_id)
        except HTTPException: 
            raise

    def get_submissions_by_question_room(self, room_code: str, question_id: int):
        try:
            return self.submission_repository.get_submissions_by_question_room(room_code, question_id)
        except HTTPException: 
            raise
