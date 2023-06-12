from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import dotenv

# openssl
env_values = dotenv.dotenv_values()
ACCESS_TOKEN_EXPIRE_MINUTES = int(env_values["ACCESS_TOKEN_EXPIRE_MINUTES"])
SECRET_KEY = env_values["SECRET_KEY"]
ALGORITHM = env_values["ALGORITHM"]


def hash_password(password: str):
    return password_context.hash(password)


def validate_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def create_jwt_token(data: dict):  # sourcery skip: dict-assign-update-to-union
    input_data = data.copy()
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    input_data.update({"exp": expiry})
    return jwt.encode(input_data, SECRET_KEY, algorithm=ALGORITHM)
