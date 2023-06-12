"""
Handles user-related operation endpoints:
- register
- get a user
- get all users
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models
from ..db_helper import get_db
from ..helpers import hash_password
from ..logger import Logger
from ..schemas import *


class DoraUser:
    """
    Handles user-related operation endpoints:
        - register
        - get a user
        - get all users
    """

    router = APIRouter(prefix="/users", tags=["User"])
    logger = Logger(__name__)

    @staticmethod
    @router.get("/{username}", response_model=RegistrationResponse)
    async def get_user(username: str, db: Session = Depends(get_db)):
        """
        Returns a user from the database.
        Success status code: 200
        Error status code: 404
        :param response:
        :param username:
        :param db:
        :return:
        """
        if (
            user := db.query(models.User)
            .filter(models.User.username == username)
            .first()
        ):
            DoraUser.logger.info(f"User {user.username} fetched.")
            return user
        DoraUser.logger.warning(f"User {username} not registered. Return 404 Exception")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username: {username} does not exist.",
        )

    @staticmethod
    @router.get("/", response_model=UserInfo)
    async def get_users(db: Session = Depends(get_db)):
        """
        Returns all registered users from the database.
        Success status code: 200
        Error status code: 400
        :param response:
        :param db:
        :return:
        """
        if users := db.query(models.User).all():
            return {"users": users}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users in the database."
        )

    @staticmethod
    @router.post(
        "/", status_code=status.HTTP_201_CREATED, response_model=RegistrationResponse
    )
    async def register(
        request: RegistrationRequest, response: Response, db: Session = Depends(get_db)
    ):
        """
        Registers the user

        :param request: Registration object
        :param response: Response object
        :param db: Database session
        :return: JSON object
        """
        request.password = hash_password(request.password)
        try:
            if user := models.User(**request.dict()):
                response.status_code = status.HTTP_201_CREATED
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
        except Exception as e:
            DoraUser.logger.warning(
                "User with this username or email already exists! Raising 405 error..."
            )
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="User with this username or email already exists! ",
            ) from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
