"""
Handle user login and authentication endpoint
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db_helper import get_db
from ..helpers import create_jwt_token, get_user, validate_password
from ..logger import Logger
from ..models import User
from ..schemas import Authentication


class DoraAuth:
    """
    Handles user login and authentication endpoints
    """

    router = APIRouter(tags=["Authentication"])
    logger = Logger(__name__)

    @staticmethod
    @router.post("/login", status_code=status.HTTP_200_OK)
    def login(credentials: Authentication, db: Session = Depends(get_db)):
        """
        Authenticates the credentials in the request
        Returns a valid JWT token if authentication is successful
        Otherwise, raises an HTTP exception with error code 403

        :param credentials: username, password
        :param db: db
        :return: jwt access token
        """
        user = db.query(User).filter(User.username == credentials.username).first()
        if not user or not validate_password(credentials.password, user.password):
            DoraAuth.logger.debug("Invalid credentials!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!"
            )
        jwt_token = create_jwt_token({"username": user.username})
        user_username = get_user(jwt_token)
        DoraAuth.logger.info(f"User logged in: {user_username}")
        return {"access_token": jwt_token, "token_type": "Bearer"}
