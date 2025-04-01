from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_google_id(self, google_id: str):
        return self.db.query(User).filter(User.google_id == google_id).first()

    def create_user(self, google_id: str, email: str, name: str):
        user = User(google_id=google_id, email=email, name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user