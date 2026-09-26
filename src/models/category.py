"""Category model for food-item classification.

Demonstrates a simple domain entity with property decorators and composition
(a FoodItem belongs to a Category).
"""


class Category:
    """A food category (e.g., Main Dish, Beverage, Snack).

    Attributes:
        category_id: Primary key from the database.
        category_name: Display name of the category.
        description: Optional description of the category.
    """

    def __init__(self, category_id: int = 0, category_name: str = "", description: str = ""):
        self._category_id = category_id
        self._category_name = category_name.strip() if isinstance(category_name, str) else category_name
        self._description = description.strip() if isinstance(description, str) else description

    @property
    def category_id(self) -> int:
        """Return the category ID."""
        return self._category_id

    @category_id.setter
    def category_id(self, value: int) -> None:
        """Return the category identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("category_id must be a non-negative integer.")
        self._category_id = value

    @property
    def category_name(self) -> str:
        """Return the category name."""
        return self._category_name

    @category_name.setter
    def category_name(self, value: str) -> None:
        """Return the category display name."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Category name cannot be empty.")
        self._category_name = value.strip()

    @property
    def description(self) -> str:
        """Return the category description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Return the category description."""
        self._description = value.strip() if isinstance(value, str) else ""

    def __str__(self) -> str:
        return f"Category(id={self._category_id}, name='{self._category_name}', desc='{self._description}')"

    def __repr__(self) -> str:
        return f"Category(category_id={self._category_id}, category_name='{self._category_name}', description='{self._description}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Category):
            return NotImplemented
        return self._category_id == other._category_id

    def __hash__(self) -> int:
        return hash(self._category_id)
