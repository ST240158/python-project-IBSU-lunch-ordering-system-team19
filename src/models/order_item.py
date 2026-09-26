"""OrderItem model — one line item within an Order.

Demonstrates **composition** (an Order is composed of OrderItem objects).
"""


class OrderItem:
    """A single line item linking an Order to a FoodItem with a quantity.

    Attributes:
        order_item_id: Primary key from the database.
        order_id: Foreign key linking to Order.
        food_item_id: Foreign key linking to FoodItem.
        item_name: Denormalised food-item name for display.
        quantity: Number of portions ordered.
        unit_price: Price per portion at time of ordering.
        subtotal: quantity × unit_price.
    """

    def __init__(
        self,
        order_item_id: int = 0,
        order_id: int = 0,
        food_item_id: int = 0,
        item_name: str = "",
        quantity: int = 1,
        unit_price: float = 0.0,
    ):
        self._order_item_id = order_item_id
        self._order_id = order_id
        self._food_item_id = food_item_id
        self._item_name = item_name
        self._quantity = quantity
        self._unit_price = unit_price

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def order_item_id(self) -> int:
        """Return the order-item identifier."""
        return self._order_item_id

    @order_item_id.setter
    def order_item_id(self, value: int) -> None:
        """Return the order-item identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("order_item_id must be a non-negative integer.")
        self._order_item_id = value

    @property
    def order_id(self) -> int:
        """Return the parent order identifier."""
        return self._order_id

    @order_id.setter
    def order_id(self, value: int) -> None:
        """Return the parent order identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("order_id must be a non-negative integer.")
        self._order_id = value

    @property
    def food_item_id(self) -> int:
        """Return the referenced food-item identifier."""
        return self._food_item_id

    @food_item_id.setter
    def food_item_id(self, value: int) -> None:
        """Return the referenced food-item identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("food_item_id must be a non-negative integer.")
        self._food_item_id = value

    @property
    def item_name(self) -> str:
        """Return the item name snapshot."""
        return self._item_name

    @item_name.setter
    def item_name(self, value: str) -> None:
        """Return the item name snapshot."""
        self._item_name = value.strip()

    @property
    def quantity(self) -> int:
        """Return the ordered quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Return the ordered quantity."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Quantity must be a positive integer.")
        self._quantity = value

    @property
    def unit_price(self) -> float:
        """Return the unit price snapshot."""
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value: float) -> None:
        """Return the unit price snapshot."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Unit price must be a non-negative number.")
        self._unit_price = round(float(value), 2)

    @property
    def subtotal(self) -> float:
        """Calculate subtotal dynamically (quantity × unit_price)."""
        return round(self._quantity * self._unit_price, 2)

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return (
            f"OrderItem(id={self._order_item_id}, item='{self._item_name}', "
            f"qty={self._quantity}, unit={self._unit_price:.2f}, "
            f"subtotal={self.subtotal:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"OrderItem(order_item_id={self._order_item_id}, "
            f"order_id={self._order_id}, food_item_id={self._food_item_id}, "
            f"quantity={self._quantity}, unit_price={self._unit_price})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderItem):
            return NotImplemented
        return self._order_item_id == other._order_item_id

    def __hash__(self) -> int:
        return hash(self._order_item_id)
