from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository

GOOGLE_CLIENT_ID = "195860473074-e880uq1l37obetripidmk7odc2kcb184.apps.googleusercontent.com"

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_google_token(self, token: str):
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            return id_info
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

    def get_or_create_user(self, token: str):
        try:
            id_info = self.verify_google_token(token)
            user = self.user_repository.get_user_by_google_id(id_info["sub"])
            if not user:
                user = self.user_repository.create_user(
                    google_id=id_info["sub"],
                    email=id_info["email"],
                    name=id_info.get("name", ""),
                )
            return user
        except HTTPException:
            raise

    def update_active_room(self, google_id: str, room_code: str):
        try:
            self.user_repository.update_active_room(google_id, room_code)
        except HTTPException:
            raise

