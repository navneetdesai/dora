"""
This file contains the database helper functions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app import models
from app.db_helper import get_db
from app.main import app
from app.settings import settings

settings = settings()
DB_URL = f"postgresql://{settings.USERNAME}:{settings.PASSWORD}@{settings.HOST}/{settings.DATABASE}_test"

engine = create_engine(DB_URL)
session_local_test = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def override_get_db():
    """
    Returns a database session
    :return: database session
    """
    db = session_local_test()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
models.Base.metadata.create_all(bind=engine)
