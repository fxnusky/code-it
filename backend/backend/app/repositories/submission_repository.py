from sqlalchemy.orm import Session
from app.models import Submission
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db
    def create_submission(self, question_id: int, player_id: int, code: str):
        try:
            submission = Submission(question_id=question_id, player_id=player_id, code=code)
            self.db.add(submission)
            self.db.commit()
            self.db.refresh(submission)
            return submission
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while creating submission"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    def update_submission_points(self, submission_id: int, new_points: int):
        try:
            submission = self.db.query(Submission).filter(Submission.submission_id == submission_id).first()
            
            if not submission:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Submission not found"
                )
                
            submission.earned_points = new_points
            self.db.commit()
            self.db.refresh(submission)
            return submission
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while updating the earned points"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error while updating the earned points"
            )