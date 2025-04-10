from app.repositories.question_repository import QuestionRepository
from fastapi import HTTPException

class QuestionService:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def get_sorted_question_ids(self, room_code: str):
        try:
            questions = self.question_repository.get_question_ids_by_room_code(room_code)
            sorted_question_ids = [question[0] for question in questions]
            return sorted_question_ids
        except HTTPException:
            raise