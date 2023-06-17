"""
This module contains helper functions for the application.
"""

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from .settings import settings

settings = settings()
SCHEME = settings.OAUTH2_SCHEME
EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
PASSWORD_CONTEXT = settings.PASSWORD_CONTEXT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def hash_password(password: str):
    """Hashes the password using bcrypt."""
    return PASSWORD_CONTEXT.hash(password)


def validate_password(password, hashed_password):
    """Validates the password using bcrypt."""
    return PASSWORD_CONTEXT.verify(password, hashed_password)


def create_jwt_token(data: dict):
    """Creates a JWT token."""
    ACCESS_TOKEN_EXPIRE_MINUTES = int(EXPIRE_MINUTES)
    input_data = data.copy()
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    input_data.update({"exp": expiry})
    return jwt.encode(input_data, SECRET_KEY, algorithm=ALGORITHM)


def _validate_jwt_token(token, invalid_credentials_exception):
    """
    Validates the JWT token.
    :param token: JWT token
    :param invalid_credentials_exception: Exception to raise if the token is invalid
    :return: username for valid token
    """

    try:
        data = jwt.decode(token, SECRET_KEY)
        if username := data.get("username"):
            return username
        else:
            raise invalid_credentials_exception
    except JWTError as e:
        raise invalid_credentials_exception from e


def get_user(token: str = Depends(SCHEME)):
    """
    Validates the JWT token and returns the username.
    :param token: JWT token
    :return: username for valid token
    """
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
    )
    return _validate_jwt_token(token, invalid_credentials_exception)
