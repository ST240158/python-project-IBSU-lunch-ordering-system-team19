"""Order model — represents a lunch order placed by a Student.

Demonstrates **composition** (contains OrderItem objects) and
**properties** for controlled attribute access.
"""

from datetime import datetime
from typing import Optional

from .order_item import OrderItem


class Order:
    """A lunch order placed by a student/customer.

    Attributes:
        order_id: Primary key from the database.
        user_id: Foreign key to the User (Student) who placed the order.
        student_name: Denormalised student name for display.
        order_date: Timestamp when the order was placed.
        status: Current order status string.
        total_amount: Sum of all item subtotals.
        items: List of OrderItem objects composing this order.
    """

    def __init__(
        self,
        order_id: int = 0,
        user_id: int = 0,
        student_name: str = "",
        order_date: Optional[str] = None,
        status: str = "received",
        total_amount: float = 0.0,
        items: Optional[list[OrderItem]] = None,
    ):
        self._order_id = order_id
        self._user_id = user_id
        self._student_name = student_name
        self._order_date = order_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._status = status
        self._total_amount = total_amount
        self._items: list[OrderItem] = items if items is not None else []

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def order_id(self) -> int:
        """Return the order identifier."""
        return self._order_id

    @order_id.setter
    def order_id(self, value: int) -> None:
        """Return the order identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("order_id must be a non-negative integer.")
        self._order_id = value

    @property
    def user_id(self) -> int:
        """Return the customer user identifier."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Return the customer user identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("user_id must be a non-negative integer.")
        self._user_id = value

    @property
    def student_name(self) -> str:
        """Return the student display name."""
        return self._student_name

    @student_name.setter
    def student_name(self, value: str) -> None:
        """Return the student display name."""
        self._student_name = value.strip()

    @property
    def order_date(self) -> str:
        """Return the order date and time."""
        return self._order_date

    @order_date.setter
    def order_date(self, value: str) -> None:
        """Return the order date and time."""
        self._order_date = value

    @property
    def status(self) -> str:
        """Return the current order status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Return the current order status."""
        valid = ("received", "preparing", "ready", "collected")
        if value not in valid:
            raise ValueError(f"Invalid status '{value}'. Must be one of {valid}.")
        self._status = value

    @property
    def total_amount(self) -> float:
        """Return the stored order total."""
        return self._total_amount

    @total_amount.setter
    def total_amount(self, value: float) -> None:
        """Return the stored order total."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("total_amount must be a non-negative number.")
        self._total_amount = round(float(value), 2)

    @property
    def items(self) -> list[OrderItem]:
        """Return the list of OrderItem objects (composition)."""
        return self._items

    # ------------------------------------------------------------------ #
    # Computed helpers                                                     #
    # ------------------------------------------------------------------ #

    @property
    def computed_total(self) -> float:
        """Sum of all item subtotals (computed dynamically)."""
        return round(sum(item.subtotal for item in self._items), 2)

    def add_item(self, item: OrderItem) -> None:
        """Add an OrderItem to this order."""
        if not isinstance(item, OrderItem):
            raise TypeError("Can only add OrderItem objects.")
        self._items.append(item)

    def remove_item(self, food_item_id: int) -> None:
        """Remove an OrderItem by its food_item_id."""
        self._items = [oi for oi in self._items if oi.food_item_id != food_item_id]

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return (
            f"Order(id={self._order_id}, student='{self._student_name}', "
            f"date={self._order_date}, status='{self._status}', "
            f"items={len(self._items)}, total={self._total_amount:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"Order(order_id={self._order_id}, user_id={self._user_id}, "
            f"status='{self._status}', items={len(self._items)})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self._order_id == other._order_id

    def __hash__(self) -> int:
        return hash(self._order_id)

    def __len__(self) -> int:
        """Number of line items in the order."""
        return len(self._items)

    def __contains__(self, item: OrderItem) -> bool:
        """Check whether an OrderItem is in this order."""
        return item in self._items
