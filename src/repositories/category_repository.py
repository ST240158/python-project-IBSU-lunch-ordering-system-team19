"""CategoryRepository — CRUD for the category table.
"""

import logging

from .database import DatabaseManager
from ..models.category import Category
from ..exceptions.custom_exceptions import DuplicateCategoryError, CategoryNotFoundError, CategoryInUseError
import sqlite3

logger = logging.getLogger("ibsu_lunch")


class CategoryRepository:
    """Data-access layer for food categories."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    def create(self, name: str, description: str = "") -> Category:
        """Insert a new category and return the domain object.

        Raises:
            DuplicateCategoryError: If the category name already exists.
        """
        existing = self._db.execute_query(
            "SELECT category_id FROM category WHERE category_name = ?", (name,)
        )
        if existing:
            raise DuplicateCategoryError(name)

        cat_id = self._db.execute_insert(
            "INSERT INTO category (category_name, description) VALUES (?, ?)",
            (name, description),
        )
        logger.info("Category created: id=%d, name='%s'.", cat_id, name)
        return Category(category_id=cat_id, category_name=name, description=description)

    def get_by_id(self, category_id: int) -> dict | None:
        """Return a category row by identifier, or None when not found."""
        rows = self._db.execute_query(
            "SELECT category_id, category_name, description FROM category WHERE category_id = ?",
            (category_id,),
        )
        if rows:
            r = rows[0]
            return {"category_id": r["category_id"], "name": r["category_name"], "description": r["description"]}
        return None

    def get_all(self) -> list[dict]:
        """Return all categories ordered by identifier."""
        rows = self._db.execute_query(
            "SELECT category_id, category_name, description FROM category ORDER BY category_id"
        )
        return [{"category_id": r["category_id"], "name": r["category_name"], "description": r["description"]} for r in rows]

    def update(self, category_id: int, name: str | None = None, description: str | None = None) -> bool:
        """Update a category's fields. Returns True if updated."""
        sets: list[str] = []
        params: list = []
        if name is not None:
            sets.append("category_name = ?")
            params.append(name)
        if description is not None:
            sets.append("description = ?")
            params.append(description)
        if not sets:
            return False
        params.append(category_id)
        sql = f"UPDATE category SET {', '.join(sets)} WHERE category_id = ?"
        count = self._db.execute_update(sql, tuple(params))
        if count == 0:
            raise CategoryNotFoundError(category_id)
        logger.info("Category id=%d updated.", category_id)
        return True

    def delete(self, category_id: int) -> bool:
        """Delete a category by identifier and return True when successful."""
        try:
            count = self._db.execute_update(
                "DELETE FROM category WHERE category_id = ?", (category_id,)
            )
        except sqlite3.IntegrityError as exc:
            raise CategoryInUseError(category_id) from exc
        if count == 0:
            raise CategoryNotFoundError(category_id)
        logger.info("Category id=%d deleted.", category_id)
        return True
