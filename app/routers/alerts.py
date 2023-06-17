"""
Handles alert endpoints
"""
import datetime
from typing import Set

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db_helper import get_db
from app.helpers import get_user
from app.logger import Logger
from app.models import Alert, Person
from app.schemas import AlertsCreateRequest
from app.settings import settings
from app.twilio_client import TwilioClient


class DoraAlert:
    """
    Handles alert endpoints
    """

    # setup router, logger, and twilio client
    router = APIRouter(tags=["Alerts"])
    logger = Logger(__name__)
    MAPPER = {
        "pincode": Person.pin_code,
        "city": Person.city,
        "state": Person.state,
        "country": Person.country,
    }
    twilio_client = TwilioClient()

    def __init__(self):
        self.numbers: Set[int] = set()
        self.emails: Set[str] = set()

    @staticmethod
    @router.post("/alerts", status_code=status.HTTP_201_CREATED)
    async def create_alert(
        request: AlertsCreateRequest,
        db: Session = Depends(get_db),
        username: str = Depends(get_user),
    ):
        """
        Create alerts
        :param request: request body
        :param db: database session
        :param username: username of current user
        :return: list of alerts created
        """
        dora_alert = DoraAlert()
        dora_alert.logger.info(f"User {username} requested to create alerts")
        await dora_alert._validate_alerts(request)
        response = dora_alert.store_alerts(request, db)
        await dora_alert.send_alerts(request, db)
        return response

    @staticmethod
    @router.get("/alerts", status_code=status.HTTP_200_OK)
    async def get_alerts(
        days: int = 1, db: Session = Depends(get_db), username: str = Depends(get_user)
    ):
        """
        Get alerts within the last n days
        :param days: number of days
        :param db: database session
        :param username: username of current user
        :return: list of alerts
        """
        DoraAlert.logger.info(f"User {username} requested alerts")
        now = datetime.datetime.now()
        from_ = now - datetime.timedelta(days=days)
        return db.query(Alert).filter(Alert.created_at.between(from_, now)).all()

    async def _validate_alerts(self, request):
        """
        Validate alerts in the request
        :param request: list of alerts
        :return: None
        """
        for alert in request.alerts:
            validation_detail = self._validate_alert(alert)
            if validation_detail is not True:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid alert: {validation_detail}",
                )

    @staticmethod
    async def _validate_alert(alert):
        """
        Validate alert
        :param alert: alert to validate
        :return: True if valid, False otherwise
        """
        is_severity_valid = alert.severity.lower() in [
            "low",
            "medium",
            "high",
            "critical",
        ]
        if not is_severity_valid:
            return "Invalid severity, must be one of: low, medium, high, critical"
        has_locations = (
            alert.cities or alert.countries or alert.states or alert.pincodes
        )
        return (
            True
            if has_locations
            else "No locations provided. Must provide at least one of: cities, countries, states, pincodes"
        )

    async def store_alerts(self, request, db):
        """
        Store alerts in the database
        :param request: request body
        :param db: database session
        :return: list of alerts created
        """
        response = []
        try:
            for alert in request.alerts:
                if existing_alert := (  # alert already exists
                    db.query(Alert)
                    .filter_by(
                        title=alert.title,
                        description=alert.description,
                        severity=alert.severity,
                    )
                    .first()
                ):  # append and log
                    response.append(existing_alert)
                    self.logger.warning(
                        "Alert already exists in the database. Skipping storage..."
                    )
                    continue
                # otherwise create new alerts
                alert_ = Alert(
                    title=alert.title,
                    description=alert.description,
                    severity=alert.severity,
                )
                db.add(alert_)
                db.commit()
                db.refresh(alert_)
                response.append(alert_)
            return response
        except Exception as e:
            self.logger.error(f"Error storing alerts: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error storing alerts: {e}",
            ) from e

    async def send_alerts(self, request, db):
        """
        Send alerts to users based on request
        :param request: request body
        :param db: database session
        :return: None
        """
        for alert in request.alerts:
            if alert.inform_all:
                self.numbers = db.query(Person.phone_number).all()
                self.emails = db.query(Person.email).all()
            else:
                # send alerts to all pincodes, cities, states, countries in request
                pincodes = alert.pincodes or []
                cities = alert.cities or []
                states = alert.states or []
                countries = alert.countries or []
                locations = [pincodes, cities, states, countries]
                types = ["pincode", "city", "state", "country"]
                for locations_, type_ in zip(locations, types):
                    if locations_:
                        await self.collect_contact_information(locations_, type_, db)
            await self.trigger_text_alerts(f"{alert.title}\n{alert.description}")
            await self.trigger_email_alerts(alert.title, alert.description)

    async def collect_contact_information(self, locations_, type_, db):
        """
        Collect contact information for the given locations
        :param locations_: list of locations
        :param type_: type of location
        :param db: database session
        :return: None
        """
        column = self.MAPPER[type_]
        # query and store numbers and emails
        for email, phone_number in (
            db.query(Person.email, Person.phone_number)
            .filter(column.in_(locations_))
            .all()
        ):
            self.numbers.add(phone_number)
            self.emails.add(email)
            self.logger.info(f"{email} will be alerted.")

    async def trigger_text_alerts(self, message="Alert from Dora"):
        """
        Send text alerts
        :param message: message to send
        :return: None
        """
        # trigger texts if flag is set and numbers are present
        if not settings().SEND_TEXTS or not self.numbers:
            self.logger.info("Skipping text alerts")
            return
        for number in self.numbers:
            self.twilio_client.send_text(message, number)
        self.logger.info(f"Text alert sent to {self.numbers}")

    async def trigger_email_alerts(self, title, description):
        """
        Send email alerts
        :param title: title of the alert
        :param description: description of the alert
        :return: None
        """
        # trigger emails if flag is set and emails are present
        if not settings().SEND_EMAILS or not self.emails:
            self.logger.info("Skipping email alerts")
            return
        for email in self.emails:
            self.twilio_client.send_email(
                f"Alert from Dora: {title}", description, email
            )
        self.logger.info(f"Email alert sent to {self.emails}")
