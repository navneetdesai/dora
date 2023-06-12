import distutils.version

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..db_helper import get_db
from ..helpers import create_jwt_token, validate_password
from ..models import User
from ..schemas import Authentication

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(credentials: Authentication, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not validate_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials."
        )
    jwt_token = create_jwt_token({"username": user.username})
    return {"access_token": jwt_token, "token_type": "Bearer"}
