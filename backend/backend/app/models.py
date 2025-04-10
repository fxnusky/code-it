from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
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
    token = Column(String)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String)
    template_id = Column(Integer, ForeignKey('game_templates.id', ondelete="CASCADE"), nullable=False)
    game_state = Column(String)

class GameTemplate(Base):
    __tablename__ = "game_templates"
    
    id = Column(Integer, primary_key=True, index=True)

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    template_id = Column(Integer, ForeignKey('game_templates.id', ondelete="CASCADE"), nullable=False)
    order_key = Column(Float, nullable=False)
    time_limit = Column(Integer, nullable=False) 
