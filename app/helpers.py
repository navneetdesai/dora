from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from .settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def hash_password(password: str):
    return password_context.hash(password)


def validate_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def create_jwt_token(data: dict):  # sourcery skip: dict-assign-update-to-union
    input_data = data.copy()
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    input_data.update({"exp": expiry})
    return jwt.encode(input_data, SECRET_KEY, algorithm=ALGORITHM)


def _validate_jwt_token(token, invalid_credentials_exception):
    try:
        data = jwt.decode(token, SECRET_KEY)
        if username := data.get("username"):
            return username
        else:
            raise invalid_credentials_exception
    except JWTError as e:
        raise invalid_credentials_exception from e


def get_user(token: str):
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
    )
    return _validate_jwt_token(token, invalid_credentials_exception)
