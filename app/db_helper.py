"""
This file contains the database helper functions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import settings

settings = settings()
DB_URL = f"postgresql://{settings.USERNAME}:{settings.PASSWORD}@{settings.HOST}/{settings.DATABASE}"

engine = create_engine(DB_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Returns a database session
    :return: database session
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()
