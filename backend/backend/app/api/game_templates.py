from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.game_template_repository import GameTemplateRepository
from ..repositories.question_repository import QuestionRepository
from ..database import get_db

router = APIRouter()


@router.get("/templates/{template_id}")
def get_template_by_id(
    template_id: int,
    db: Session = Depends(get_db)
):
    template_repository = GameTemplateRepository(db)
    
    try:
        template = template_repository.get_template_by_id(template_id)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "detail": f"Template with ID {template_id} retrieved correctly",
            "data": {
                "template": template
            }
            
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )