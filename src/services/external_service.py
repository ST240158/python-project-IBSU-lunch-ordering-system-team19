"""External HTTP service integration for the IBSU Lunch Ordering System."""

import logging
from datetime import datetime

import requests

from ..exceptions.custom_exceptions import IBSUAppError

logger = logging.getLogger("ibsu_lunch")


class ExternalServiceError(IBSUAppError):
    """Raised when an external HTTP service cannot be reached or parsed."""

    def __init__(self, service_name: str, reason: str) -> None:
        self.service_name = service_name
        self.reason = reason
        super().__init__(
            f"External service '{service_name}' failed: {reason}"
        )


class ExternalTimeService:
    """Retrieves current Port Moresby time from an external HTTP API.

    The service is intentionally isolated from the core ordering workflow.
    If the external service is unavailable, the lunch ordering system
    continues to operate normally.
    """

    API_URL = (
        "https://worldtimeapi.org/api/timezone/"
        "Pacific/Port_Moresby"
    )
    SERVICE_NAME = "World Time API"
    TIMEOUT_SECONDS = 5

    def get_current_time(self) -> dict:
        """Fetch current Port Moresby time using an HTTP GET request.

        Returns:
            Dictionary containing the external service status,
            timezone, current datetime and UTC offset.

        Raises:
            ExternalServiceError: If the HTTP request fails or the
                response cannot be interpreted.
        """
        try:
            response = requests.get(
                self.API_URL,
                timeout=self.TIMEOUT_SECONDS,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "IBSU-Lunch-Ordering-System/1.0",
                },
            )

            response.raise_for_status()

            data = response.json()

            datetime_value = data.get("datetime")
            timezone = data.get("timezone")
            utc_offset = data.get("utc_offset")

            if not datetime_value or not timezone:
                raise ExternalServiceError(
                    self.SERVICE_NAME,
                    "The response did not contain the expected time data.",
                )

            # Validate that the returned value is a valid ISO datetime.
            datetime.fromisoformat(datetime_value.replace("Z", "+00:00"))

            logger.info(
                "External time service succeeded: timezone=%s status=%s",
                timezone,
                response.status_code,
            )

            return {
                "service": self.SERVICE_NAME,
                "status_code": response.status_code,
                "available": True,
                "timezone": timezone,
                "datetime": datetime_value,
                "utc_offset": utc_offset,
            }

        except requests.Timeout as exc:
            logger.warning(
                "External time service timed out after %s seconds.",
                self.TIMEOUT_SECONDS,
            )
            raise ExternalServiceError(
                self.SERVICE_NAME,
                "The service request timed out.",
            ) from exc

        except requests.RequestException as exc:
            logger.warning(
                "External time service request failed: %s",
                exc,
            )
            raise ExternalServiceError(
                self.SERVICE_NAME,
                "The service could not be reached.",
            ) from exc

        except (ValueError, TypeError) as exc:
            logger.warning(
                "Invalid response from external time service: %s",
                exc,
            )
            raise ExternalServiceError(
                self.SERVICE_NAME,
                "The service returned invalid data.",
            ) from exc