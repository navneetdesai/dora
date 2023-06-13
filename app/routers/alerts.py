from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from app.db_helper import get_db
from app.logger import Logger
from app.schemas import AlertsCreateRequest


class DoraAlert:
    """
    Handles alert endpoints
    """

    router = APIRouter(tags=["Alerts"])
    logger = Logger(__name__)

    @router.post("/alerts", status_code=status.HTTP_201_CREATED)
    async def create_alert(
        self, request: AlertsCreateRequest, db: Session = Depends(get_db)
    ):
        pass
        # await self._validate_alerts(request) and self.logger.info("Alerts validated")

    async def _validate_alerts(self, request):
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
        is_severity_valid = (
            alert.severity.lower() in "critical",
            "high",
            "medium",
            "low",
        )
        is_coverage_valid = 0 <= alert.coverage < 10, 000
        return is_severity_valid and is_coverage_valid
