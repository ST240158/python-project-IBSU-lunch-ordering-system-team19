"""MainController — application entry point / main loop.

Orchestrates login, role-based routing, and session lifecycle.
"""

import logging
import sys

from ..services.auth_service import AuthService
from ..services.report_service import ReportService
from ..services.file_service import FileService
from ..views.main_view import MainView
from ..views.student_view import StudentView
from ..views.admin_view import AdminView
from ..controllers.student_controller import StudentController
from ..controllers.admin_controller import AdminController
from ..repositories.user_repository import UserRepository
from ..repositories.category_repository import CategoryRepository
from ..repositories.food_item_repository import FoodItemRepository
from ..repositories.order_repository import OrderRepository
from ..repositories.order_item_repository import OrderItemRepository
from ..repositories.order_status_repository import OrderStatusRepository
from ..repositories.database import DatabaseManager
from ..exceptions.custom_exceptions import InvalidCredentialsError, DuplicateUsernameError, InvalidInputError
from ..utils.validators import validate_username, validate_password, validate_name

logger = logging.getLogger("ibsu_lunch")


class MainController:
    """Top-level controller that drives the main application loop."""

    def __init__(self, db: DatabaseManager | None = None) -> None:
        self._db = db or DatabaseManager()
        self._db.initialize_schema()

        self._user_repo = UserRepository(self._db)
        self._category_repo = CategoryRepository(self._db)
        self._food_repo = FoodItemRepository(self._db)
        self._order_item_repo = OrderItemRepository(self._db)
        self._status_repo = OrderStatusRepository(self._db)
        self._order_repo = OrderRepository(
            self._db,
            self._food_repo,
            self._order_item_repo,
            self._status_repo,
        )
        self._file_svc = FileService()

        self._auth = AuthService(self._user_repo)
        self._report = ReportService(
            self._order_repo, self._food_repo, self._category_repo, self._file_svc
        )

        self._main_view = MainView()
        self._student_view = StudentView()
        self._admin_view = AdminView()

        self._student_ctrl: StudentController | None = None
        self._admin_ctrl: AdminController | None = None

        self._running = True

    def run(self) -> None:
        """Start the main application loop."""
        self._main_view.show_banner()
        # Seed default data if tables are empty
        self._seed_if_empty()

        while self._running:
            choice = self._main_view.show_main_menu()
            if choice == "1":
                self._handle_login(expected_role="student")
            elif choice == "2":
                self._handle_login(expected_role="admin")
            elif choice == "3":
                self._running = False
                self._main_view.show_goodbye()
            else:
                self._main_view.show_error("Invalid choice. Please enter 1-3.")

    # ------------------------------------------------------------------ #
    # Login / Registration                                                #
    # ------------------------------------------------------------------ #

    def _handle_login(self, expected_role: str | None = None) -> None:
        username, password = self._main_view.prompt_login()
        try:
            user = self._auth.login(username, password)
            if expected_role is not None and user.role != expected_role:
                self._main_view.show_error("The account role does not match this login option.")
                return
            self._main_view.show_success(f"Welcome, {user.name}!")
            if user.role == "student":
                self._launch_student_session(user)
            elif user.role == "admin":
                self._launch_admin_session(user)
            else:
                self._main_view.show_error("Unknown role.")
        except InvalidCredentialsError as exc:
            self._main_view.show_error(str(exc))

    def _launch_student_session(self, user) -> None:
        self._student_ctrl = StudentController(
            user=user,
            food_repo=self._food_repo,
            category_repo=self._category_repo,
            order_repo=self._order_repo,
            order_item_repo=self._order_item_repo,
            status_repo=self._status_repo,
            user_repo=self._user_repo,
            file_svc=self._file_svc,
            view=self._student_view,
        )
        self._student_ctrl.run()

    def _launch_admin_session(self, user) -> None:
        self._admin_ctrl = AdminController(
            user=user,
            food_repo=self._food_repo,
            category_repo=self._category_repo,
            order_repo=self._order_repo,
            order_item_repo=self._order_item_repo,
            status_repo=self._status_repo,
            user_repo=self._user_repo,
            report=self._report,
            file_svc=self._file_svc,
            view=self._admin_view,
        )
        self._admin_ctrl.run()

    # ------------------------------------------------------------------ #
    # Database seeding                                                     #
    # ------------------------------------------------------------------ #

    def _seed_if_empty(self) -> None:
        """Insert default categories and admin if the database is empty."""
        categories = self._category_repo.get_all()
        if not categories:
            seed_cats = [
                {"name": "Main Dish", "description": "Hearty main courses"},
                {"name": "Side Dish", "description": "Accompaniments and sides"},
                {"name": "Beverage", "description": "Drinks and refreshments"},
                {"name": "Dessert", "description": "Sweet treats"},
                {"name": "Salad", "description": "Fresh salads"},
            ]
            for cat in seed_cats:
                self._category_repo.create(cat["name"], cat["description"])
            logger.info("Seeded %d default categories.", len(seed_cats))

        admins = self._user_repo.get_by_role("admin")
        if not admins:
            self._user_repo.create_admin("admin", "admin123", "System Administrator")
            logger.info("Seeded default admin account (admin / admin123).")

        items = self._food_repo.get_all()
        if not items:
            all_cats = self._category_repo.get_all()
            cat_map = {c["name"]: c["category_id"] for c in all_cats}
            seed_items = [
                {"category_id": cat_map.get("Main Dish", 1), "name": "Grilled Chicken", "description": "Juicy grilled chicken breast", "price": 7.50, "stock": 50},
                {"category_id": cat_map.get("Main Dish", 1), "name": "Beef Stew", "description": "Hearty beef stew with vegetables", "price": 8.00, "stock": 40},
                {"category_id": cat_map.get("Main Dish", 1), "name": "Vegetable Pasta", "description": "Penne with seasonal veggies", "price": 6.50, "stock": 35},
                {"category_id": cat_map.get("Side Dish", 2), "name": "French Fries", "description": "Crispy golden fries", "price": 3.00, "stock": 80},
                {"category_id": cat_map.get("Side Dish", 2), "name": "Mashed Potatoes", "description": "Creamy mashed potatoes", "price": 3.50, "stock": 60},
                {"category_id": cat_map.get("Beverage", 3), "name": "Orange Juice", "description": "Fresh-squeezed orange juice", "price": 2.50, "stock": 100},
                {"category_id": cat_map.get("Beverage", 3), "name": "Coffee", "description": "Hot brewed coffee", "price": 2.00, "stock": 120},
                {"category_id": cat_map.get("Beverage", 3), "name": "Mineral Water", "description": "Still mineral water", "price": 1.50, "stock": 200},
                {"category_id": cat_map.get("Dessert", 4), "name": "Chocolate Cake", "description": "Rich chocolate layer cake", "price": 4.50, "stock": 30},
                {"category_id": cat_map.get("Dessert", 4), "name": "Fruit Salad", "description": "Mixed seasonal fruits", "price": 3.50, "stock": 45},
                {"category_id": cat_map.get("Salad", 5), "name": "Caesar Salad", "description": "Classic Caesar with croutons", "price": 5.50, "stock": 40},
                {"category_id": cat_map.get("Salad", 5), "name": "Greek Salad", "description": "Tomatoes, cucumber, olives, feta", "price": 5.00, "stock": 35},
            ]
            for item in seed_items:
                self._food_repo.create(
                    item["category_id"], item["name"], item["description"],
                    item["price"], item["stock"]
                )
            logger.info("Seeded %d default menu items.", len(seed_items))

        # Seed a demo student
        students = self._user_repo.get_by_role("student")
        if not students:
            self._user_repo.create_student("student", "student123", "Demo Student", "student@ibsu.edu")
            logger.info("Seeded demo student account (student / student123).")
