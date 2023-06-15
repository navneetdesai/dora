import datetime
from typing import Set

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.openapi.models import Response
from psycopg2 import errors
from sqlalchemy.orm import Session

from app.db_helper import get_db
from app.geopy_helper import Geopy
from app.helpers import get_user
from app.logger import Logger
from app.models import Alert, Person, Region
from app.schemas import AlertsCreateRequest
from app.settings import settings
from app.twilio_client import TwilioClient


class DoraAlert:
    """
    Handles alert endpoints
    """

    router = APIRouter(tags=["Alerts"])
    logger = Logger(__name__)
    geo = Geopy()
    numbers: Set[int] = set()
    emails: Set[str] = set()
    mapper = {
        "pincode": Person.pin_code,
        "city": Person.city,
        "state": Person.state,
        "country": Person.country,
    }
    twilio_client = None

    @staticmethod
    @router.post("/alerts", status_code=status.HTTP_201_CREATED)
    async def create_alert(
        request: AlertsCreateRequest,
        db: Session = Depends(get_db),
        username: str = Depends(get_user),
    ):
        dora_alert = DoraAlert()
        dora_alert.twilio_client = TwilioClient()
        dora_alert.numbers.clear()
        dora_alert.emails.clear()
        dora_alert._validate_alerts(request)
        dora_alert.logger.info("Alerts validated")
        response = dora_alert.store_alerts(request, db)
        dora_alert.logger.info("Alerts stored")
        dora_alert.send_alerts(request, db)
        return response

    @staticmethod
    @router.get("/alerts", status_code=status.HTTP_200_OK)
    async def get_alerts(
        days: int = 1, db: Session = Depends(get_db), username: str = Depends(get_user)
    ):
        now = datetime.datetime.now()
        from_ = now - datetime.timedelta(days=days)
        return db.query(Alert).filter(Alert.created_at.between(from_, now)).all()

    def _validate_alerts(self, request):
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
    def _validate_alert(alert):
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

    def store_alerts(self, request, db):
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

    def send_alerts(self, request, db):
        for alert in request.alerts:
            if alert.inform_all:
                # make twilio calls
                pass
            # send alerts to all pincodes, cities, states, countries in request
            pincodes = alert.pincodes or []
            cities = alert.cities or []
            states = alert.states or []
            countries = alert.countries or []
            locations = [pincodes, cities, states, countries]
            types = ["pincode", "city", "state", "country"]
            for locations_, type_ in zip(locations, types):
                if locations_:
                    self.collect_contact_information(locations_, type_, db)
            self.trigger_text_alerts(f"{alert.title}\n{alert.description}")
            self.trigger_email_alerts(alert.title, alert.description)

    def collect_contact_information(self, locations_, type_, db):
        column = self.mapper[type_]
        for email, phone_number in (
            db.query(Person.email, Person.phone_number)
            .filter(column.in_(locations_))
            .all()
        ):
            self.numbers.add(phone_number)
            self.emails.add(email)
            self.logger.info(f"{email} will be alerted.")

    def trigger_text_alerts(self, message="Alert from Dora"):
        # for number in self.numbers:
        if not settings.send_texts or not self.numbers:
            self.logger.info("Skipping text alerts")
            return
        for number in self.numbers:
            self.twilio_client.send_text(message, number)
        self.logger.info(f"Text alert sent to {self.numbers}")

    def trigger_email_alerts(self, title, description):
        if not settings.send_emails or not self.emails:
            self.logger.info("Skipping email alerts")
            return
        for email in self.emails:
            self.twilio_client.send_email(
                f"Alert from Dora: {title}", description, email
            )
        self.logger.info(f"Email alert sent to {self.emails}")
