from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from . import models
from .db_helper import engine, get_db, session_local
from .queries import Query
from .schemas import Registration

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/users/{username}")
async def get_user(username: str, response: Response, db: Session = Depends(get_db)):
    """
    Returns a user from the database.
    Success status code: 200
    Error status code: 404
    :param response:
    :param username:
    :param db:
    :return:
    """
    if user := db.query(models.User).filter(models.User.username == username).first():
        return {"data": user}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "User not found"}


@app.get("/users")
async def get_users(response: Response, db: Session = Depends(get_db)):
    """
    Returns all registered users from the database.
    Success status code: 200
    Error status code: 400
    :param response:
    :param db:
    :return:
    """
    if user := db.query(models.User).all():
        return {"data": user}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "No registered users found"}


@app.post("/register")
async def register(
    item: Registration, response: Response, db: Session = Depends(get_db)
):
    """
    Registers the user

    :param item: Registration object
    :param response: Response object
    :param db: Database session
    :return: JSON object
    """
    if user := models.User(**item.dict()):
        response.status_code = status.HTTP_201_CREATED
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"data": user}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "User already exists"}
