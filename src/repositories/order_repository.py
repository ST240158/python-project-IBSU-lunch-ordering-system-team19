"""OrderRepository — full CRUD for orders, plus search and reporting queries.

Uses transactions for multi-step operations (creating an order with its
line items atomically, decreasing stock; cancelling and restoring stock).
"""

import logging
from datetime import datetime

from .database import DatabaseManager
from .food_item_repository import FoodItemRepository
from .order_item_repository import OrderItemRepository
from .order_status_repository import OrderStatusRepository
from ..models.order import Order
from ..models.order_item import OrderItem
from ..exceptions.custom_exceptions import (
    OrderNotFoundError,
    InsufficientStockError,
    OrderCannotBeCancelledError,
    InvalidOrderError,
)

logger = logging.getLogger("ibsu_lunch")


class OrderRepository:
    """Data-access layer for lunch orders."""

    def __init__(
        self,
        db: DatabaseManager,
        food_repo: FoodItemRepository | None = None,
        order_item_repo: OrderItemRepository | None = None,
        order_status_repo: OrderStatusRepository | None = None,
    ) -> None:
        self._db = db
        self._food_repo = food_repo
        self._order_item_repo = order_item_repo
        self._status_repo = order_status_repo

    # ------------------------------------------------------------------ #
    # Create (transactional)                                               #
    # ------------------------------------------------------------------ #

    def create(self, user_id: int, status_id: int, items: list[dict]) -> int:
        """Create a new order with line items and decrease stock atomically.

        Args:
            user_id: The placing student's user ID.
            status_id: Initial status ID (typically 1 = received).
            items: List of dicts with keys ``food_item_id``, ``quantity``,
                   ``name``, ``price``.

        Returns:
            The new order_id.

        Raises:
            InsufficientStockError: If any item has insufficient stock.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Compute total
        total = 0.0
        for it in items:
            subtotal = it["price"] * it["quantity"]
            total += subtotal
        total = round(total, 2)

        conn = self._db.connection
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (user_id, order_date, status_id, total_amount) "
                "VALUES (?, ?, ?, ?)",
                (user_id, now, status_id, total),
            )
            order_id = cursor.lastrowid

            # Insert order items
            for it in items:
                subtotal = round(it["price"] * it["quantity"], 2)
                cursor.execute(
                    "INSERT INTO order_items "
                    "(order_id, food_item_id, item_name, quantity, unit_price, subtotal) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (order_id, it["food_item_id"], it["name"], it["quantity"], it["price"], subtotal),
                )

            # Decrease stock
            for it in items:
                cursor.execute(
                    "UPDATE food_items SET stock = stock - ? "
                    "WHERE food_item_id = ? AND stock >= ?",
                    (it["quantity"], it["food_item_id"], it["quantity"]),
                )
                if cursor.rowcount == 0:
                    conn.rollback()
                    raise InsufficientStockError(it["name"], it["quantity"], 0)

            conn.commit()
            logger.info("Order id=%d created (user=%d, total=%.2f).", order_id, user_id, total)
            return order_id
        except InsufficientStockError:
            raise
        except Exception:
            conn.rollback()
            raise

    # ------------------------------------------------------------------ #
    # Read                                                                 #
    # ------------------------------------------------------------------ #

    def get_by_id(self, order_id: int) -> dict | None:
        """Return an order row dict (with student name and status)."""
        rows = self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE o.order_id = ?",
            (order_id,),
        )
        return rows[0] if rows else None

    def get_by_student(self, user_id: int) -> list[dict]:
        """Return all orders for a student, newest first."""
        return self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE o.user_id = ? ORDER BY o.order_date DESC",
            (user_id,),
        )

    def get_all(self) -> list[dict]:
        """Return all orders, newest first."""
        return self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "ORDER BY o.order_date DESC"
        )

    # ------------------------------------------------------------------ #
    # Search / filter                                                      #
    # ------------------------------------------------------------------ #

    def search_by_date(self, date_str: str) -> list[dict]:
        """Return orders placed on a given date (YYYY-MM-DD)."""
        return self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE DATE(o.order_date) = ? ORDER BY o.order_date DESC",
            (date_str,),
        )

    def search_by_status(self, status_name: str) -> list[dict]:
        """Return orders matching an exact status name."""
        return self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE os.status_name = ? ORDER BY o.order_date DESC",
            (status_name,),
        )

    def search_by_student_name(self, keyword: str) -> list[dict]:
        """Return orders whose student name contains the keyword."""
        return self._db.execute_query(
            "SELECT o.order_id, o.user_id, u.name AS student_name, "
            "o.order_date, os.status_name AS status, o.total_amount "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE u.name LIKE ? ORDER BY o.order_date DESC",
            (f"%{keyword}%",),
        )

    # ------------------------------------------------------------------ #
    # Update                                                               #
    # ------------------------------------------------------------------ #

    def update_status(self, order_id: int, status_id: int) -> bool:
        """Update an order's status by status_id.

        Raises:
            OrderNotFoundError: If the order does not exist.
        """
        count = self._db.execute_update(
            "UPDATE orders SET status_id = ? WHERE order_id = ?",
            (status_id, order_id),
        )
        if count == 0:
            raise OrderNotFoundError(order_id)
        logger.info("Order id=%d status updated to status_id=%d.", order_id, status_id)
        return True

    def cancel_order(self, order_id: int, user_id: int | None = None) -> bool:
        """Cancel an eligible received order transactionally.

        The project defines exactly four persistent statuses and no cancelled
        status. Cancellation is therefore represented by removing the order
        and restoring its reserved stock.
        """
        order = self.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        if user_id is not None and order["user_id"] != user_id:
            raise InvalidOrderError("This order does not belong to you.")
        if order["status"] != "received":
            raise OrderCannotBeCancelledError(order_id, order["status"])
        items = self._order_item_repo.get_by_order_id(order_id) if self._order_item_repo else []
        conn = self._db.connection
        try:
            cursor = conn.cursor()
            for item in items:
                cursor.execute(
                    "UPDATE food_items SET stock = stock + ? WHERE food_item_id = ?",
                    (item["quantity"], item["food_item_id"]),
                )
            cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise OrderNotFoundError(order_id)
            conn.commit()
            logger.info("Order id=%d cancelled; order removed and stock restored.", order_id)
            return True
        except Exception:
            conn.rollback()
            raise

    def delete(self, order_id: int) -> bool:
        """Delete an order and its line items in a single transaction.

        received/preparing orders restore their reserved stock before deletion;
        later-stage orders do not restore stock because fulfilment has progressed.

        Raises:
            OrderNotFoundError: If the order does not exist.
        """
        order = self.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)

        items = self._order_item_repo.get_by_order_id(order_id) if self._order_item_repo else []
        conn = self._db.connection
        try:
            cursor = conn.cursor()
            if order["status"] in ("received", "preparing"):
                for item in items:
                    cursor.execute(
                        "UPDATE food_items SET stock = stock + ? WHERE food_item_id = ?",
                        (item["quantity"], item["food_item_id"]),
                    )
            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
            cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise OrderNotFoundError(order_id)
            conn.commit()
            logger.info("Order id=%d deleted.", order_id)
            return True
        except OrderNotFoundError:
            raise
        except Exception:
            conn.rollback()
            raise

    # ------------------------------------------------------------------ #
    # Reporting queries                                                    #
    # ------------------------------------------------------------------ #

    def get_daily_sales(self, date: str | None = None) -> list[dict]:
        """Return completed-order rows for a given date.

        Each row: order_id, student_name, total_amount, status.
        """
        target = date or datetime.now().strftime("%Y-%m-%d")
        return self._db.execute_query(
            "SELECT o.order_id, u.name AS student_name, o.total_amount, os.status_name AS status "
            "FROM orders o "
            "JOIN users u ON o.user_id = u.user_id "
            "JOIN order_status os ON o.status_id = os.status_id "
            "WHERE DATE(o.order_date) = ? AND os.status_name = 'collected' "
            "ORDER BY o.order_date DESC",
            (target,),
        )

    def get_popular_items(self, limit: int = 10) -> list[dict]:
        """Return the most ordered food items by total quantity."""
        return self._db.execute_query(
            "SELECT oi.food_item_id, oi.item_name AS name, SUM(oi.quantity) AS total_qty, "
            "SUM(oi.subtotal) AS revenue "
            "FROM order_items oi "
            "JOIN orders o ON oi.order_id = o.order_id "
            ""
            "GROUP BY oi.food_item_id ORDER BY total_qty DESC LIMIT ?",
            (limit,),
        )

    def get_category_sales(self) -> list[dict]:
        """Return sales grouped by category."""
        return self._db.execute_query(
            "SELECT c.category_id, c.category_name AS category_name, "
            "SUM(oi.subtotal) AS total_revenue, "
            "COUNT(DISTINCT o.order_id) AS order_count "
            "FROM order_items oi "
            "JOIN food_items f ON oi.food_item_id = f.food_item_id "
            "JOIN category c ON f.category_id = c.category_id "
            "JOIN orders o ON oi.order_id = o.order_id "
            ""
            "GROUP BY c.category_id ORDER BY total_revenue DESC"
        )

    def get_order_status_summary(self) -> list[dict]:
        """Return count of orders by status."""
        return self._db.execute_query(
            "SELECT os.status_name, COUNT(o.order_id) AS count "
            "FROM order_status os "
            "LEFT JOIN orders o ON os.status_id = o.status_id "
            "GROUP BY os.status_id ORDER BY os.status_id"
        )
