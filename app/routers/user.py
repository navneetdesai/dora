from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models
from ..db_helper import get_db
from ..helpers import hash_password
from ..schemas import *

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/{username}", response_model=UserInfo)
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
        return user
    response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with username: {username} does not exist.",
    )


@router.get("/")
async def get_users(response: Response, db: Session = Depends(get_db)):
    """
    Returns all registered users from the database.
    Success status code: 200
    Error status code: 400
    :param response:
    :param db:
    :return:
    """
    if users := db.query(models.User).all():
        return {"data": users}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No users in the database."
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=RegistrationResponse
)
async def register(
    item: RegistrationRequest, response: Response, db: Session = Depends(get_db)
):
    """
    Registers the user

    :param item: Registration object
    :param response: Response object
    :param db: Database session
    :return: JSON object
    """
    item.password = hash_password(item.password)
    if user := models.User(**item.dict()):
        response.status_code = status.HTTP_201_CREATED
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
