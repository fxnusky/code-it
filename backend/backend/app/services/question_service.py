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
    
    def get_question_by_id(self, question_id: int):
        try:
            question = self.question_repository.get_question_by_id(question_id)
            return {
                "id": question.id,
                "description": question.description,
                "time_limit": question.time_limit,
                "code_starter": question.code_starter
            }
        except HTTPException:
            raise