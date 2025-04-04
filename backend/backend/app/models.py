from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    active_room = Column(String)
    
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    room_code = Column(String)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String)