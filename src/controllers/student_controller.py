"""StudentController — handles the Student / Customer session loop.
"""

import logging

from ..models.user import User
from ..repositories.food_item_repository import FoodItemRepository
from ..repositories.category_repository import CategoryRepository
from ..repositories.order_repository import OrderRepository
from ..repositories.order_item_repository import OrderItemRepository
from ..repositories.order_status_repository import OrderStatusRepository
from ..repositories.user_repository import UserRepository
from ..services.file_service import FileService
from ..views.student_view import StudentView
from ..exceptions.custom_exceptions import InsufficientStockError, OrderNotFoundError, InvalidOrderError

logger = logging.getLogger("ibsu_lunch")


class StudentController:
    """Drives the student-facing workflow after login."""

    def __init__(
        self,
        user: User,
        food_repo: FoodItemRepository,
        category_repo: CategoryRepository,
        order_repo: OrderRepository,
        order_item_repo: OrderItemRepository,
        status_repo: OrderStatusRepository,
        user_repo: UserRepository,
        file_svc: FileService,
        view: StudentView,
    ) -> None:
        self._user = user
        self._food_repo = food_repo
        self._category_repo = category_repo
        self._order_repo = order_repo
        self._order_item_repo = order_item_repo
        self._status_repo = status_repo
        self._user_repo = user_repo
        self._file_svc = file_svc
        self._view = view

    def run(self) -> None:
        """Main student session loop."""
        while True:
            choice = self._view.show_student_menu(self._user.name)
            if choice == "1":
                self._browse_menu()
            elif choice == "2":
                self._search_food()
            elif choice == "3":
                self._place_order()
            elif choice == "4":
                self._view_my_orders()
            elif choice == "5":
                self._cancel_order()
            elif choice == "6":
                self._view.show_info("Logged out successfully.")
                break
            else:
                self._view.show_error("Invalid choice. Please enter 1-6.")

    # ------------------------------------------------------------------ #
    # Browse menu                                                          #
    # ------------------------------------------------------------------ #

    def _browse_menu(self) -> None:
        items = self._food_repo.get_all()
        categories = self._category_repo.get_all()
        self._view.show_menu_table(items, categories)

    # ------------------------------------------------------------------ #
    # Search food
    # ------------------------------------------------------------------ #

    def _search_food(self) -> None:
        keyword = self._view.prompt_search()
        results = self._food_repo.search(keyword)
        self._view.show_menu_table(results)

    # ------------------------------------------------------------------ #
    # Place order                                                          #
    # ------------------------------------------------------------------ #

    def _place_order(self) -> None:
        self._browse_menu()
        selected = self._view.prompt_order_items()
        if not selected:
            self._view.show_info("No items selected. Order cancelled.")
            return

        # Validate items and compute total
        order_lines: list[dict] = []
        total = 0.0
        for sel in selected:
            item = self._food_repo.get_by_id(sel["food_item_id"])
            if item is None:
                self._view.show_error(f"Food item ID {sel['food_item_id']} not found.")
                return
            if sel["quantity"] <= 0:
                self._view.show_error(f"Invalid quantity for {item['name']}.")
                return
            if item["stock"] < sel["quantity"]:
                self._view.show_error(f"Insufficient stock for {item['name']} (available: {item['stock']}).")
                return
            subtotal = item["price"] * sel["quantity"]
            order_lines.append({
                "food_item_id": item["food_item_id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": sel["quantity"],
                "subtotal": subtotal,
            })
            total += subtotal

        if not self._view.confirm_order(total):
            self._view.show_info("Order cancelled.")
            return

        try:
             # received is the initial order status
            received = self._status_repo.get_by_name("received")
            order_id = self._order_repo.create(self._user.user_id, received["status_id"], order_lines) if received else None
            if order_id is None:
                self._view.show_error("Order status configuration is unavailable.")
                return
            self._view.show_success(f"Order #{order_id} placed! Total: K{total:.2f}")
        except InsufficientStockError as exc:
            self._view.show_error(str(exc))
        except Exception as exc:
            logger.error("Order creation failed: %s", exc)
            self._view.show_error("Could not place order. Please try again.")

    # ------------------------------------------------------------------ #
    # View orders                                                          #
    # ------------------------------------------------------------------ #

    def _view_my_orders(self) -> None:
        orders = self._order_repo.get_by_student(self._user.user_id)
        self._view.show_orders(orders)

    # ------------------------------------------------------------------ #
    # Cancel order                                                         #
    # ------------------------------------------------------------------ #

    def _cancel_order(self) -> None:
        self._view_my_orders()
        order_id = self._view.prompt_cancel_order()
        if order_id is None:
            return
        try:
            self._order_repo.cancel_order(order_id, self._user.user_id)
            self._view.show_success(f"Order #{order_id} has been cancelled.")
        except OrderNotFoundError as exc:
            self._view.show_error(str(exc))
        except InvalidOrderError as exc:
            self._view.show_error(str(exc))

    # ------------------------------------------------------------------ #
    # View profile                                                         #
    # ------------------------------------------------------------------ #

    def _view_profile(self) -> None:
        user_data = self._user_repo.get_by_id(self._user.user_id)
        if user_data:
            self._view.show_profile(user_data)
        else:
            self._view.show_error("Could not load profile.")
