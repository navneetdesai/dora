from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from app.db_helper import get_db
from app.logger import Logger
from app.models import Alert
from app.schemas import AlertsCreateRequest


class DoraAlert:
    """
    Handles alert endpoints
    """

    router = APIRouter(tags=["Alerts"])
    logger = Logger(__name__)

    @staticmethod
    @router.post("/alerts", status_code=status.HTTP_201_CREATED)
    async def create_alert(request: AlertsCreateRequest, db: Session = Depends(get_db)):
        dora_alert = DoraAlert()
        dora_alert._validate_alerts(request)
        dora_alert.logger.info("Alerts validated")
        dora_alert.store_alerts(request, db)
        return None

    def _validate_alerts(self, request):
        for alert in request.alerts:
            if not self._validate_alert(alert):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid alert: {alert}",
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
        print(type(alert.coverage))
        is_coverage_valid = 0 <= alert.coverage < 10000
        print(is_coverage_valid)
        return is_severity_valid and is_coverage_valid

    def store_alerts(self, request, db):
        try:
            for alert in request.alerts:
                alert_ = Alert(
                    title=alert.title,
                    description=alert.description,
                    severity=alert.severity,
                    coverage=alert.coverage,
                )
                db.add(alert_)
                db.commit()
                db.refresh(alert_)
        except Exception as e:
            self.logger.error(f"Error storing alerts: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error storing alerts: {e}",
            )
