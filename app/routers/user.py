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
from ..schemas import RegistrationRequest, RegistrationResponse, UserInfo


class DoraUser:
    """
    Handles user-related operation endpoints:
        - register
        - get a user
        - get all users
    """

    # set up router and logger
    router = APIRouter(prefix="/users", tags=["User"])
    logger = Logger(__name__)

    @staticmethod
    @router.get("/{username}", response_model=RegistrationResponse)
    async def get_user(username: str, db_session: Session = Depends(get_db)):
        """
        Returns a user from the database.
        Success status code: 200
        Error status code: 404
        :param db_session: Database session
        :param username: username of the user
        :return: JSON object
        """
        if (  # return user if present in the database
            user := db_session.query(models.User)
            .filter(models.User.username == username)
            .first()
        ):
            DoraUser.logger.info("User %s fetched.", user.username)
            return user
        DoraUser.logger.warning(
            "User %s not registered. Return 404 Exception", username
        )
        raise HTTPException(  # raise 404 exception if user not present in the database
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username: {username} does not exist.",
        )

    @staticmethod
    @router.get("/", response_model=UserInfo)
    async def get_users(db_session: Session = Depends(get_db)):
        """
        Returns all registered users from the database.
        Success status code: 200
        Error status code: 400
        :param db_session: Database session
        :return: JSON object
        """
        if users := db_session.query(models.User).all():
            return {"users": users}
        DoraUser.logger.warning("No users in the database. Return 404 Exception")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users in the database."
        )

    @staticmethod
    @router.post(
        "/", status_code=status.HTTP_201_CREATED, response_model=RegistrationResponse
    )
    async def register(
        request: RegistrationRequest,
        response: Response,
        db_session: Session = Depends(get_db),
    ):
        """
        Registers the user

        :param request: Registration object
        :param response: Response object
        :param db_session: Database session
        :return: JSON object
        """
        request.password = hash_password(request.password)
        try:
            if user := models.User(**request.dict()):
                response.status_code = status.HTTP_201_CREATED
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
                return user
        except Exception as exception:
            DoraUser.logger.warning(
                "User with this username or email already exists! Raising 405 error..."
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username or email already exists! ",
            ) from exception
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
