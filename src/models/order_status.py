"""OrderStatus model — represents the status of an order.

The canonical status values match the project prompt: received, preparing, ready, collected.
"""


class OrderStatus:
    """A status value that can be assigned to an Order.

    Attributes:
        status_id: Primary key from the database.
        status_name: Display name (e.g., 'received').
    """

    VALID_STATUSES = ("received", "preparing", "ready", "collected")

    def __init__(self, status_id: int = 0, status_name: str = ""):
        self._status_id = status_id
        self._status_name = status_name

    @property
    def status_id(self) -> int:
        """Return the status identifier."""
        return self._status_id

    @status_id.setter
    def status_id(self, value: int) -> None:
        """Return the status identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("status_id must be a non-negative integer.")
        self._status_id = value

    @property
    def status_name(self) -> str:
        """Return the status display name."""
        return self._status_name

    @status_name.setter
    def status_name(self, value: str) -> None:
        """Return the status display name."""
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{value}'. Must be one of {self.VALID_STATUSES}."
            )
        self._status_name = value

    def __str__(self) -> str:
        return f"OrderStatus(id={self._status_id}, name='{self._status_name}')"

    def __repr__(self) -> str:
        return f"OrderStatus(status_id={self._status_id}, status_name='{self._status_name}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderStatus):
            return NotImplemented
        return self._status_id == other._status_id

    def __hash__(self) -> int:
        return hash(self._status_id)
