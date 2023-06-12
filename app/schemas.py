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


class UserInfo(Registration):
    pass
