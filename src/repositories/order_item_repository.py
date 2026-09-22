"""OrderItemRepository — CRUD for the order_items table.
"""

import logging

from .database import DatabaseManager
from ..models.order_item import OrderItem

logger = logging.getLogger("ibsu_lunch")


class OrderItemRepository:
    """Data-access layer for order line items."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    def create(self, order_id: int, food_item_id: int, item_name: str,
               quantity: int, unit_price: float, subtotal: float) -> int:
        """Insert an order-item row and return its ID."""
        oid = self._db.execute_insert(
            "INSERT INTO order_items (order_id, food_item_id, item_name, quantity, unit_price, subtotal) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, food_item_id, item_name, quantity, unit_price, subtotal),
        )
        logger.debug("OrderItem created: id=%d, order=%d.", oid, order_id)
        return oid

    def get_by_order_id(self, order_id: int) -> list[dict]:
        """Return all items for a given order as row dicts."""
        return self._db.execute_query(
            "SELECT order_item_id, order_id, food_item_id, item_name, quantity, unit_price, subtotal "
            "FROM order_items WHERE order_id = ?",
            (order_id,),
        )

    def get_all(self) -> list[dict]:
        """Return all order-item rows ordered by order identifier."""
        return self._db.execute_query(
            "SELECT order_item_id, order_id, food_item_id, item_name, quantity, unit_price, subtotal "
            "FROM order_items ORDER BY order_id"
        )

    def delete_by_order_id(self, order_id: int) -> int:
        """Delete all items for an order. Returns rowcount."""
        return self._db.execute_update(
            "DELETE FROM order_items WHERE order_id = ?", (order_id,)
        )
