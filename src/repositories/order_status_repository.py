"""OrderStatusRepository — read-only access to the order_status table.
"""

from .database import DatabaseManager


class OrderStatusRepository:
    """Data-access layer for order statuses (read-only reference data)."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    def get_all(self) -> list[dict]:
        """Return all available order statuses."""
        return self._db.execute_query(
            "SELECT status_id, status_name FROM order_status ORDER BY status_id"
        )

    def get_by_id(self, status_id: int) -> dict | None:
        """Return an order status row by identifier, or None."""
        rows = self._db.execute_query(
            "SELECT status_id, status_name FROM order_status WHERE status_id = ?",
            (status_id,),
        )
        return rows[0] if rows else None

    def get_by_name(self, status_name: str) -> dict | None:
        """Return an order status row by name, or None."""
        rows = self._db.execute_query(
            "SELECT status_id, status_name FROM order_status WHERE status_name = ?",
            (status_name,),
        )
        return rows[0] if rows else None
