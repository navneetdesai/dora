"""
Handles subscriber endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from .. import models
from ..db_helper import get_db
from ..helpers import get_user, hash_password
from ..logger import Logger
from ..schemas import *


class DoraSubscriber:
    """
    Handles subscriber endpoints
    """

    router = APIRouter(tags=["User"])
    logger = Logger(__name__)

    @staticmethod
    @router.post("/subscribe", status_code=status.HTTP_201_CREATED)
    async def subscribe(
        request: Subscriber,
        db: Session = Depends(get_db),
        username: str = Depends(get_user),
    ):
        """
        Registers a subscriber in the database.
        Success status code: 201
        Error status code: 500
        :param username: username of the user
        :param request: request body
        :param db: Database session
        :return: JSON object
        """
        DoraSubscriber.logger.info(
            f"Registering subscriber {request.email} from {username}'s request."
        )
        try:
            subscriber = models.Person(
                first_name=request.first_name,
                last_name=request.last_name,
                language=request.language,
                phone_number=request.phone_number,
                email=request.email,
                pin_code=request.pin_code,
                city=request.city,
                state=request.state,
                country=request.country,
            )
            db.add(subscriber)
            db.commit()
            db.refresh(subscriber)
            DoraSubscriber.logger.info(f"Subscriber {subscriber.email} registered.")
            return subscriber
        except Exception as e:
            DoraSubscriber.logger.error(
                f"Subscriber {request.email} registration failed."
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Subscriber {request.email} registration failed due to internal server error.",
            ) from e

    @staticmethod
    @router.get(
        "/subscribers", response_model=Subscribers, status_code=status.HTTP_200_OK
    )
    async def get_subscribers(
        email: str = Query(None),
        pin_code: str = Query(None),
        city: str = Query(None),
        db: Session = Depends(get_db),
        username: str = Depends(get_user),
    ):
        """
        Returns all subscribers in the database.
        Success status code: 200
        Error status code: 500
        :param city: city of the subscriber
        :param pin_code: pin code of the subscriber
        :param email: email of the subscriber
        :param username: username of the user
        :param db: Database session
        :return: JSON object
        """
        DoraSubscriber.logger.info(f"Retrieving subscribers for {username}'s request.")
        try:
            subscribers = db.query(models.Person)
            if email:
                subscribers = subscribers.filter(models.Person.email == email)
            if pin_code:
                subscribers = subscribers.filter(models.Person.pin_code == pin_code)
            if city:
                subscribers = subscribers.filter(models.Person.city == city)
            subscribers = subscribers.all()
            DoraSubscriber.logger.info("Subscribers fetched.")
            return {"subscribers": subscribers}
        except Exception as e:
            DoraSubscriber.logger.error("Subscribers fetch failed.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Subscribers fetch failed.",
            ) from e
