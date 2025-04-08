from app.repositories.room_repository import RoomRepository
from app.models import Room
import random

class RoomService:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository
    
    def get_room_code(self):
        existing_room_codes = self.room_repository.get_existing_room_codes()
        
        while True:
            room_code = f"{random.randint(0, 999999):06d}"
            if room_code not in existing_room_codes:
                return room_code
    
    def create_room(self, room_code, template_id):
        return self.room_repository.create_room(room_code, template_id)


