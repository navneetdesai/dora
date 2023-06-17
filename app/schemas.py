"""
Define the schemas for the API
"""
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Registration(BaseModel):
    """
    Base schema for user registration
    """

    username: str
    email: EmailStr
    first_name: str
    last_name: str


class RegistrationRequest(Registration):
    """
    Schema for user registration request
    """

    password: str


class RegistrationResponse(Registration):
    """
    Schema for user registration response
    """

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    """
    Schema for users info
    """

    users: Optional[List[RegistrationResponse]]

    class Config:
        orm_mode = True


class Authentication(BaseModel):
    """
    Base schema for user authentication
    """

    username: str
    password: str


class JWTToken(BaseModel):
    """
    Schema for JWT token
    """

    username: Optional[str]


class AlertCreateRequest(BaseModel):
    """
    Schema for a single alert

    """

    title: str
    description: str
    severity: str
    pincodes: Optional[List[int]]
    cities: Optional[List[str]]
    states: Optional[List[str]]
    countries: Optional[List[str]]
    inform_all: Optional[bool] = False


class AlertsCreateRequest(BaseModel):
    """
    Schema for alerts creation request
    """

    alerts: List[AlertCreateRequest]


class Subscriber(BaseModel):
    """
    Schema for a single subscriber
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    language: str
    pin_code: int
    city: str
    state: str
    country: str

    class Config:
        orm_mode = True


class Subscribers(BaseModel):
    """
    Schema for subscribers
    """

    subscribers: Optional[List[Subscriber]]

    class Config:
        orm_mode = True
