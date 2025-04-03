from pydantic import BaseModel

class PlayerCreate(BaseModel):
    room_code: str
    nickname: str