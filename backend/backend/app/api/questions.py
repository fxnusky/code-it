from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.question_repository import QuestionRepository
from ..database import get_db

router = APIRouter()

@router.get("/questions/{question_id}")
def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):
    question_repository = QuestionRepository(db)
    
    try:
        question = question_repository.get_question_by_id(question_id)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "detail": f"Question with ID {question_id} retrieved correctly",
            "data": {
                "question": question
            }
            
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
