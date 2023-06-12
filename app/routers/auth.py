from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..db_helper import get_db
from ..helpers import create_jwt_token, get_user, validate_password
from ..models import User
from ..schemas import Authentication


class DoraAuth:
    router = APIRouter(tags=["Authentication"])

    @staticmethod
    @router.post("/login")
    def login(credentials: Authentication, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == credentials.username).first()
        if not user or not validate_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials."
            )
        jwt_token = create_jwt_token({"username": user.username})
        user = get_user(jwt_token)
        print(user)
        return {"access_token": jwt_token, "token_type": "Bearer"}
