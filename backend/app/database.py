from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

engine = create_engine(os.getenv("DATABASE_URL"), pool_size=200, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()