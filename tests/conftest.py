"""Shared pytest fixtures for the IBSU Lunch Ordering System.

Provides an in-memory SQLite database with the schema pre-initialised,
plus repository and service instances wired to that database.
"""

import os
import sys
import pytest
import tempfile

# Ensure the project root is on sys.path so ``src`` is importable.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.repositories.database import DatabaseManager
from src.repositories.user_repository import UserRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.food_item_repository import FoodItemRepository
from src.repositories.order_item_repository import OrderItemRepository
from src.repositories.order_status_repository import OrderStatusRepository
from src.repositories.order_repository import OrderRepository
from src.services.auth_service import AuthService
from src.services.file_service import FileService
from src.services.report_service import ReportService


# --------------------------------------------------------------------------- #
# Database fixtures                                                            #
# --------------------------------------------------------------------------- #

@pytest.fixture()
def db(tmp_path):
    """Return a DatabaseManager backed by a temp file, schema pre-loaded."""
    db_path = str(tmp_path / "test_lunch.db")
    dm = DatabaseManager(db_path)
    dm.initialize_schema()
    yield dm
    dm.close()


@pytest.fixture()
def user_repo(db):
    return UserRepository(db)


@pytest.fixture()
def category_repo(db):
    return CategoryRepository(db)


@pytest.fixture()
def food_repo(db):
    return FoodItemRepository(db)


@pytest.fixture()
def order_item_repo(db):
    return OrderItemRepository(db)


@pytest.fixture()
def order_status_repo(db):
    return OrderStatusRepository(db)


@pytest.fixture()
def order_repo(db, food_repo, order_item_repo, order_status_repo):
    return OrderRepository(db, food_repo, order_item_repo, order_status_repo)


# --------------------------------------------------------------------------- #
# Service fixtures                                                            #
# --------------------------------------------------------------------------- #

@pytest.fixture()
def auth_service(user_repo):
    return AuthService(user_repo)


@pytest.fixture()
def file_service(tmp_path):
    """Return a FileService whose base directory is a temp folder."""
    base = str(tmp_path / "data")
    return FileService(base)


@pytest.fixture()
def report_service(order_repo, food_repo, category_repo, file_service):
    return ReportService(order_repo, food_repo, category_repo, file_service)


# --------------------------------------------------------------------------- #
# Seed data helpers                                                           #
# --------------------------------------------------------------------------- #

@pytest.fixture()
def seed_admin(user_repo):
    """Create and return a default admin."""
    return user_repo.create_admin("admin", "admin123", "System Admin")


@pytest.fixture()
def seed_student(user_repo):
    """Create and return a default student."""
    return user_repo.create_student("student1", "student123", "Alice Smith", "alice@ibsu.edu")


@pytest.fixture()
def seed_categories(category_repo):
    """Create 3 categories and return them as a list of dicts."""
    cats = []
    for name, desc in [("Main Dish", "Hearty mains"), ("Beverage", "Drinks"), ("Dessert", "Sweets")]:
        cats.append(category_repo.create(name, desc))
    return cats


@pytest.fixture()
def seed_food_items(food_repo, category_repo):
    """Create categories + food items and return the food-item dicts."""
    c1 = category_repo.create("Main Dish", "Mains")
    c2 = category_repo.create("Beverage", "Drinks")
    items = [
        food_repo.create(c1.category_id, "Chicken Rice", "Chicken with rice", 5.50, 20),
        food_repo.create(c1.category_id, "Beef Stew", "Beef stew with bread", 6.00, 15),
        food_repo.create(c2.category_id, "Orange Juice", "Fresh OJ", 2.50, 50),
    ]
    return items


@pytest.fixture()
def seed_order(order_repo, user_repo, food_repo, category_repo, order_status_repo):
    """Create a student, food item, and a pending order — return the order_id."""
    student = user_repo.create_student("s1", "pass123", "Bob", "bob@ibsu.edu")
    cat = category_repo.create("Main Dish", "Mains")
    item = food_repo.create(cat.category_id, "Pasta", "Penne pasta", 5.00, 30)
    pending = order_status_repo.get_by_name("received")
    items = [{"food_item_id": item.food_item_id, "name": item.name, "price": item.price, "quantity": 2}]
    order_id = order_repo.create(student.user_id, pending["status_id"], items)
    return order_id, student, item