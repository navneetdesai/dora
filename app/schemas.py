from pydantic import BaseModel


class Registration(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
