from sqlalchemy.orm import Session
from app.models import Submission, TestCaseExecution, Player, TestCase
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, case, select

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
    
    def get_submission(self, player_id: int, question_id: int):
        try:
            return self.db.query(Submission).filter(Submission.player_id == player_id, Submission.question_id == question_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the submission"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    def get_submissions_by_submission_id(self, submission_id: int):
        try:
            return self.db.query(Submission).filter(Submission.submission_id == submission_id).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the submission"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    
    def get_total_points_by_player_id(self, player_id: int):
        try:
            points = ( self.db.query(func.sum(Submission.earned_points))\
                     .filter(Submission.player_id == player_id)\
                     .scalar()
            )
            if points:
                return points
            return 0
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the submission"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    
    def get_question_results_stats(self, room_code: str, question_id: int):
        try:
            players_in_room = self.db.query(Player.id).where(Player.room_code == room_code).scalar_subquery()
            num_players_in_room =  self.db.query(Player.id).where(Player.room_code == room_code).count()

            results = (
                self.db.query(
                    TestCaseExecution.case_id,
                    (func.sum(
                        case(
                            (TestCaseExecution.correct == True, 1.0),
                            else_=0.0
                        )
                    ) * 100).label("percentage_correct")
                )
                .join(Submission, TestCaseExecution.submission_id == Submission.submission_id)
                .filter(
                    Submission.question_id == question_id,
                    Submission.player_id.in_(players_in_room)
                )
                .group_by(TestCaseExecution.case_id)
                .order_by(TestCaseExecution.case_id)
                .all()
            )
            if results and num_players_in_room:
                return [{"case_id": int(row.case_id), "percentage_correct": float(row.percentage_correct/num_players_in_room)} for row in results]
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
                detail="Database error while retrieving the question stats"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        
    def get_total_points_players(self, room_code: str):
        try:

            players_points = (
                self.db.query(
                    Submission.player_id,
                    func.sum(Submission.earned_points).label("total_points")
                )
                .filter(Submission.player_id.in_(
                    self.db.query(Player.id).where(Player.room_code == room_code)
                ))
                .group_by(Submission.player_id)
                .all()
            )

            return  {player_id: total_points for player_id, total_points in players_points}
        
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the question stats"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    def get_submissions_by_question_room(self, room_code: str, question_id: int):
        try:
            stmt = (
                select(func.count(Submission.submission_id))
                .join(Player, Submission.player_id == Player.id)
                .where(
                    Player.room_code == room_code,
                    Submission.question_id == question_id
                )
            )
            return self.db.scalar(stmt)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while retrieving the amount of submissions"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )