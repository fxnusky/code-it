from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, Boolean, TIMESTAMP
from .database import Base
from sqlalchemy.sql import func

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
    code_starter = Column(Text, nullable=False)
    main_function = Column(Text, nullable=False)
    language = Column(Text, nullable=False, default='python')

class TestCase(Base):
    __tablename__ = 'test_cases'

    case_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete="CASCADE"))
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)

class Submission(Base):
    __tablename__ = 'submissions'

    submission_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, nullable=False)
    code = Column(Text, nullable=False)
    earned_points = Column(Integer, nullable=False, default=0)
    submission_time = Column(TIMESTAMP, server_default=func.now())

class TestCaseExecution(Base):
    __tablename__ = 'test_case_executions'

    case_execution_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.submission_id', ondelete="CASCADE"), nullable=False)
    case_id = Column(Integer, ForeignKey('test_cases.case_id', ondelete="CASCADE"), nullable=False)
    obtained_output = Column(Text, nullable=False)
    correct = Column(Boolean, nullable=False)
