"""FoodItem model — represents a menu item offered by the cafeteria.

Demonstrates **composition** (belongs to a Category), **properties** for
controlled attribute access, and **dunder methods**.
"""


class FoodItem:
    """A food/menu item available for ordering.

    Attributes:
        food_item_id: Primary key from the database.
        name: Display name of the food item.
        category_id: Foreign key linking to Category.
        category_name: Denormalised category name for display.
        description: Optional description of the item.
        price: Unit price (non-negative float rounded to 2 dp).
        stock: Number of portions available.
    """

    def __init__(
        self,
        food_item_id: int = 0,
        name: str = "",
        category_id: int = 0,
        category_name: str = "",
        description: str = "",
        price: float = 0.0,
        stock: int = 0,
    ):
        self._food_item_id = food_item_id
        self._name = name.strip() if isinstance(name, str) else name
        self._category_id = category_id
        self._category_name = category_name.strip() if isinstance(category_name, str) else category_name
        self._description = description.strip() if isinstance(description, str) else description
        self._price = round(float(price), 2) if isinstance(price, (int, float)) else price
        self._stock = stock

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def food_item_id(self) -> int:
        """Return the food-item ID."""
        return self._food_item_id

    @food_item_id.setter
    def food_item_id(self, value: int) -> None:
        """Return the food-item identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("food_item_id must be a non-negative integer.")
        self._food_item_id = value

    @property
    def name(self) -> str:
        """Return the food-item name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Return the food-item display name."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Food item name cannot be empty.")
        self._name = value.strip()

    @property
    def category_id(self) -> int:
        """Return the category foreign key."""
        return self._category_id

    @category_id.setter
    def category_id(self, value: int) -> None:
        """Return the category foreign-key identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("category_id must be a non-negative integer.")
        self._category_id = value

    @property
    def category_name(self) -> str:
        """Return the denormalised category name."""
        return self._category_name

    @category_name.setter
    def category_name(self, value: str) -> None:
        """Return the category display name."""
        self._category_name = value.strip()

    @property
    def description(self) -> str:
        """Return the item description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Return the food-item description."""
        self._description = value.strip() if isinstance(value, str) else ""

    @property
    def price(self) -> float:
        """Return the unit price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Return the unit price."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = round(float(value), 2)

    @property
    def stock(self) -> int:
        """Return the number of portions available."""
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        """Return the available stock quantity."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Stock must be a non-negative integer.")
        self._stock = value

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return (
            f"FoodItem(id={self._food_item_id}, name='{self._name}', "
            f"category='{self._category_name}', price={self._price:.2f}, "
            f"stock={self._stock})"
        )

    def __repr__(self) -> str:
        return (
            f"FoodItem(food_item_id={self._food_item_id}, name='{self._name}', "
            f"category_id={self._category_id}, price={self._price}, "
            f"stock={self._stock})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FoodItem):
            return NotImplemented
        return self._food_item_id == other._food_item_id

    def __hash__(self) -> int:
        return hash(self._food_item_id)
