"""FoodItemRepository — CRUD, search, and stock management for food_items.
"""

import logging

from .database import DatabaseManager
from ..models.food_item import FoodItem
from ..exceptions.custom_exceptions import FoodItemNotFoundError, InsufficientStockError

logger = logging.getLogger("ibsu_lunch")


class FoodItemRepository:
    """Data-access layer for food items on the menu."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    def create(self, category_id: int, name: str, description: str = "", price: float = 0.0, stock: int = 0) -> FoodItem:
        """Insert a new food item and return the domain object."""
        item_id = self._db.execute_insert(
            "INSERT INTO food_items (category_id, name, description, price, stock) "
            "VALUES (?, ?, ?, ?, ?)",
            (category_id, name, description, price, stock),
        )
        logger.info("Food item created: id=%d, name='%s'.", item_id, name)
        return FoodItem(food_item_id=item_id, category_id=category_id, name=name, description=description, price=price, stock=stock)

    def get_by_id(self, food_item_id: int) -> dict | None:
        """Return a food-item row by identifier, or None when not found."""
        rows = self._db.execute_query(
            "SELECT food_item_id, category_id, name, description, price, stock "
            "FROM food_items WHERE food_item_id = ?",
            (food_item_id,),
        )
        return rows[0] if rows else None

    def get_all(self) -> list[dict]:
        """Return all food items ordered by category and name."""
        return self._db.execute_query(
            "SELECT food_item_id, category_id, name, description, price, stock "
            "FROM food_items ORDER BY category_id, name"
        )

    def search(self, keyword: str) -> list[dict]:
        """Search food items by name or description (case-insensitive)."""
        return self._db.execute_query(
            "SELECT food_item_id, category_id, name, description, price, stock "
            "FROM food_items WHERE name LIKE ? OR description LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"),
        )

    def update(self, food_item_id: int, **kwargs) -> bool:
        """Update a food item's fields. Returns True if updated.

        Accepted keyword args: name, description, price, stock, category_id
        """
        allowed = {"name", "description", "price", "stock", "category_id"}
        sets: list[str] = []
        params: list = []
        for key, val in kwargs.items():
            if key in allowed and val is not None:
                sets.append(f"{key} = ?")
                params.append(val)
        if not sets:
            return False
        params.append(food_item_id)
        sql = f"UPDATE food_items SET {', '.join(sets)} WHERE food_item_id = ?"
        count = self._db.execute_update(sql, tuple(params))
        if count == 0:
            raise FoodItemNotFoundError(food_item_id)
        logger.info("Food item id=%d updated.", food_item_id)
        return True

    def delete(self, food_item_id: int) -> bool:
        """Delete a food item by identifier and return True when successful."""
        count = self._db.execute_update(
            "DELETE FROM food_items WHERE food_item_id = ?", (food_item_id,)
        )
        if count == 0:
            raise FoodItemNotFoundError(food_item_id)
        logger.info("Food item id=%d deleted.", food_item_id)
        return True

    def decrease_stock(self, food_item_id: int, quantity: int) -> bool:
        """Atomically decrease stock. Raises InsufficientStockError if not enough."""
        item = self.get_by_id(food_item_id)
        if item is None:
            raise FoodItemNotFoundError(food_item_id)
        if item["stock"] < quantity:
            raise InsufficientStockError(item["name"], quantity, item["stock"])
        count = self._db.execute_update(
            "UPDATE food_items SET stock = stock - ? WHERE food_item_id = ? AND stock >= ?",
            (quantity, food_item_id, quantity),
        )
        if count == 0:
            raise InsufficientStockError(item["name"], quantity, item["stock"])
        logger.info("Stock decreased: item=%d qty=%d.", food_item_id, quantity)
        return True

    def increase_stock(self, food_item_id: int, quantity: int) -> bool:
        """Increase stock (used when orders are cancelled)."""
        count = self._db.execute_update(
            "UPDATE food_items SET stock = stock + ? WHERE food_item_id = ?",
            (quantity, food_item_id),
        )
        if count == 0:
            raise FoodItemNotFoundError(food_item_id)
        return True
