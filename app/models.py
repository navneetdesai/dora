from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .db_helper import Base


class User(Base):
    """
    Users of the API
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Person(Base):
    """
    People who are in the system
    """

    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    language = Column(String, nullable=True, default="en")
    pin_code = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)


class Region(Base):
    """
    Regions that are in the system
    """

    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    geocode = Column(String, nullable=False)


class Alert(Base):
    """
    Stores historical alerts
    """

    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    severity = Column(String)
    __table_args__ = (
        UniqueConstraint("title", "description", "severity", name="uix_1"),
    )
