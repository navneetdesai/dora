from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Registration(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str


class RegistrationRequest(Registration):
    password: str


class RegistrationResponse(Registration):
    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    users: Optional[List[RegistrationResponse]]

    class Config:
        orm_mode = True


class Authentication(BaseModel):
    username: str
    password: str


class JWTToken(BaseModel):
    username: Optional[str]
