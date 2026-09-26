"""AdminController — handles the Administrator session loop.
"""

import logging

from ..models.user import User
from ..repositories.food_item_repository import FoodItemRepository
from ..repositories.category_repository import CategoryRepository
from ..repositories.order_repository import OrderRepository
from ..repositories.order_item_repository import OrderItemRepository
from ..repositories.order_status_repository import OrderStatusRepository
from ..repositories.user_repository import UserRepository
from ..services.report_service import ReportService
from ..services.file_service import FileService
from ..views.admin_view import AdminView
from ..services.external_service import ExternalTimeService
from ..services.external_service import (
    ExternalTimeService,
    ExternalServiceError,
)
from ..exceptions.custom_exceptions import (
    InsufficientStockError, OrderNotFoundError, FileOperationError,
    ReportGenerationError, DuplicateCategoryError, CategoryNotFoundError,
    CategoryInUseError,
)

logger = logging.getLogger("ibsu_lunch")


class AdminController:
    """Drives the admin-facing workflow after login."""

    def __init__(
        self,
        user: User,
        food_repo: FoodItemRepository,
        category_repo: CategoryRepository,
        order_repo: OrderRepository,
        order_item_repo: OrderItemRepository,
        status_repo: OrderStatusRepository,
        user_repo: UserRepository,
        report: ReportService,
        file_svc: FileService,
        external_service: ExternalTimeService,
        view: AdminView,
    ) -> None:
        self._user = user
        self._food_repo = food_repo
        self._category_repo = category_repo
        self._order_repo = order_repo
        self._order_item_repo = order_item_repo
        self._status_repo = status_repo
        self._user_repo = user_repo
        self._report = report
        self._file_svc = file_svc
        self._external_service = external_service
        self._view = view

    def run(self) -> None:
        """Main admin session loop."""
        while True:
            choice = self._view.show_admin_menu(self._user.name)
            if choice == "1":
                self._add_menu_item()
            elif choice == "2":
                self._view_all_menu_items()
            elif choice == "3":
                self._update_menu_item()
            elif choice == "4":
                self._delete_menu_item()
            elif choice == "5":
                self._view_orders_with_search()
            elif choice == "6":
                self._update_order_status()
            elif choice == "7":
                self._report_management()
            elif choice == "8":
                self._view.show_info("Logged out successfully.")
                break
            else:
                self._view.show_error("Invalid choice. Please enter 1-8.")

    # ================================================================== #
    # MENU ITEM MANAGEMENT                                                #
    # ================================================================== #

    def _menu_item_management(self) -> None:
        while True:
            choice = self._view.show_menu_item_submenu()
            if choice == "1":
                self._add_menu_item()
            elif choice == "2":
                self._update_menu_item()
            elif choice == "3":
                self._delete_menu_item()
            elif choice == "4":
                self._view_all_menu_items()
            elif choice == "5":
                self._search_menu_items()
            elif choice == "6":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _add_menu_item(self) -> None:
        categories = self._category_repo.get_all()
        if not categories:
            self._view.show_error("No categories exist. Please create a category first.")
            return
        try:
            data = self._view.prompt_add_menu_item(categories)
            if data["price"] < 0:
                self._view.show_error("Price cannot be negative.")
                return
            if data["stock"] < 0:
                self._view.show_error("Stock cannot be negative.")
                return
            self._food_repo.create(data["category_id"], data["name"], data["description"], data["price"], data["stock"])
            self._view.show_success(f"Menu item '{data['name']}' added.")
        except Exception as exc:
            self._view.show_error(str(exc))

    def _update_menu_item(self) -> None:
        items = self._food_repo.get_all()
        data = self._view.prompt_update_menu_item(items)
        if data is None:
            return
        try:
            self._food_repo.update(
                data["food_item_id"],
                name=data.get("name"),
                description=data.get("description"),
                price=data.get("price"),
                stock=data.get("stock"),
                category_id=data.get("category_id"),
            )
            self._view.show_success(f"Menu item #{data['food_item_id']} updated.")
        except Exception as exc:
            self._view.show_error(str(exc))

    def _delete_menu_item(self) -> None:
        item_id = self._view.prompt_delete_menu_item()
        if item_id is None:
            return
        try:
            self._food_repo.delete(item_id)
            self._view.show_success(f"Menu item #{item_id} deleted.")
        except Exception as exc:
            self._view.show_error(str(exc))

    def _view_all_menu_items(self) -> None:
        items = self._food_repo.get_all()
        self._view.show_food_items_table(items)

    def _search_menu_items(self) -> None:
        keyword = self._view.prompt_search()
        results = self._food_repo.search(keyword)
        self._view.show_food_items_table(results, title=f"🔍 Search Results for '{keyword}'")

    # ================================================================== #
    # CATEGORY MANAGEMENT                                                 #
    # ================================================================== #

    def _category_management(self) -> None:
        while True:
            choice = self._view.show_category_submenu()
            if choice == "1":
                self._add_category()
            elif choice == "2":
                self._update_category()
            elif choice == "3":
                self._delete_category()
            elif choice == "4":
                self._view_all_categories()
            elif choice == "5":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _add_category(self) -> None:
        data = self._view.prompt_add_category()
        try:
            self._category_repo.create(data["name"], data["description"])
            self._view.show_success(f"Category '{data['name']}' added.")
        except DuplicateCategoryError as exc:
            self._view.show_error(str(exc))

    def _update_category(self) -> None:
        categories = self._category_repo.get_all()
        data = self._view.prompt_update_category(categories)
        if data is None:
            return
        try:
            self._category_repo.update(data["category_id"], name=data.get("name"), description=data.get("description"))
            self._view.show_success(f"Category #{data['category_id']} updated.")
        except CategoryNotFoundError as exc:
            self._view.show_error(str(exc))

    def _delete_category(self) -> None:
        cat_id = self._view.prompt_delete_category()
        if cat_id is None:
            return
        try:
            self._category_repo.delete(cat_id)
            self._view.show_success(f"Category #{cat_id} deleted.")
        except CategoryNotFoundError as exc:
            self._view.show_error(str(exc))
        except CategoryInUseError as exc:
            self._view.show_error(str(exc))

    def _view_all_categories(self) -> None:
        categories = self._category_repo.get_all()
        self._view.show_categories_table(categories)

    # ================================================================== #
    # ORDER MANAGEMENT                                                    #
    # ================================================================== #

    def _view_all_orders(self) -> None:
        orders = self._order_repo.get_all()
        self._view.show_orders_table(orders)

    def _view_orders_with_search(self) -> None:
        """View all orders and optionally search by student, date, or status."""
        self._view_all_orders()
        print("  Search: 1=Student, 2=Date, 3=Status, 4=Back")
        choice = input("  Search option: ").strip()
        if choice == "1":
            results = self._order_repo.search_by_student_name(input("  Student name: ").strip())
            self._view.show_orders_table(results, "Search Results")
        elif choice == "2":
            results = self._order_repo.search_by_date(input("  Date (YYYY-MM-DD): ").strip())
            self._view.show_orders_table(results, "Search Results")
        elif choice == "3":
            statuses = self._status_repo.get_all()
            status = input("  Status (received/preparing/ready/collected): ").strip().lower()
            match = next((x for x in statuses if x["status_name"].lower() == status), None)
            if not match:
                self._view.show_error("Invalid order status.")
                return
            results = self._order_repo.search_by_status(match["status_name"])
            self._view.show_orders_table(results, "Search Results")

    def _update_order_status(self) -> None:
        result = self._view.prompt_update_order_status()
        if result is None:
            return
        order_id, status_id = result
        try:
            self._order_repo.update_status(order_id, status_id)
            self._view.show_success(f"Order #{order_id} status updated to status_id={status_id}.")
        except OrderNotFoundError as exc:
            self._view.show_error(str(exc))

    def _delete_order(self) -> None:
        """Delete an order after confirmation and restore eligible stock."""
        order_id = self._view.prompt_delete_order()
        if order_id is None:
            return
        try:
            self._order_repo.delete(order_id)
            self._view.show_success(f"Order #{order_id} deleted.")
        except OrderNotFoundError as exc:
            self._view.show_error(str(exc))
        except Exception as exc:
            logger.exception("Order deletion failed for id=%s.", order_id)
            self._view.show_error(str(exc))

    # ================================================================== #
    # REPORTS                                                             #
    # ================================================================== #

    def _report_management(self) -> None:
        while True:
            choice = self._view.show_report_submenu()
            if choice == "1":
                self._daily_sales_report()
            elif choice == "2":
                self._popular_items_report()
            elif choice == "3":
                self._category_revenue_report()
            elif choice == "4":
                self._generate_charts()
            elif choice == "5":
                self._export_full_report()
            elif choice == "6":
                self._external_service_check()
            elif choice == "7":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _daily_sales_report(self) -> None:
        date = self._view.prompt_report_date() or None
        try:
            df = self._report.get_daily_sales_dataframe(date)
            self._view.show_dataframe(df, "Daily Sales Report")
        except ReportGenerationError as exc:
            self._view.show_error(str(exc))

    def _popular_items_report(self) -> None:
        try:
            df = self._report.get_popular_items_dataframe()
            self._view.show_dataframe(df, "Popular Items Report")
        except ReportGenerationError as exc:
            self._view.show_error(str(exc))

    def _category_revenue_report(self) -> None:
        try:
            df = self._report.get_category_sales_dataframe()
            self._view.show_dataframe(df, "Category Revenue Report")
        except ReportGenerationError as exc:
            self._view.show_error(str(exc))

    def _generate_charts(self) -> None:
        date = self._view.prompt_report_date() or None
        try:
            paths = {}
            bar_path = self._report.plot_daily_sales_bar(date)
            if bar_path:
                paths["Daily Sales Bar"] = bar_path
            pie_path = self._report.plot_popular_items_pie()
            if pie_path:
                paths["Popular Items Pie"] = pie_path
            cat_path = self._report.plot_category_sales_bar()
            if cat_path:
                paths["Category Revenue Bar"] = cat_path
            self._view.show_chart_paths(paths)
        except ReportGenerationError as exc:
            self._view.show_error(str(exc))

    def _export_full_report(self) -> None:
        date = self._view.prompt_report_date() or None
        try:
            result = self._report.export_full_report(date)
            self._view.show_success(f"Report exported: {result}")
        except ReportGenerationError as exc:
            self._view.show_error(str(exc))

    # ================================================================== #
    # IMPORT / EXPORT                                                     #
    # ================================================================== #

    def _import_menu(self) -> None:
        while True:
            choice = self._view.show_import_submenu()
            if choice == "1":
                self._import_csv()
            elif choice == "2":
                self._import_json()
            elif choice == "3":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _import_csv(self) -> None:
        filename = self._view.prompt_import_filename("csv")
        filepath = self._file_svc.get_import_path(filename)
        try:
            rows = self._file_svc.import_csv(filepath)
            count = 0
            for row in rows:
                try:
                    cat_id = int(row.get("category_id", 1))
                    name = row.get("name", "")
                    desc = row.get("description", "")
                    price = float(row.get("price", 0))
                    stock = int(row.get("stock", 0))
                    if name:
                        self._food_repo.create(cat_id, name, desc, price, stock)
                        count += 1
                except Exception:
                    logger.warning("Skipping CSV row: %s", row)
            self._view.show_success(f"Imported {count} menu items from CSV.")
        except FileOperationError as exc:
            self._view.show_error(str(exc))

    def _import_json(self) -> None:
        filename = self._view.prompt_import_filename("json")
        filepath = self._file_svc.get_import_path(filename)
        try:
            data = self._file_svc.import_json(filepath)
            count = 0
            items = data if isinstance(data, list) else data.get("items", [])
            for item in items:
                try:
                    cat_id = int(item.get("category_id", 1))
                    name = item.get("name", "")
                    desc = item.get("description", "")
                    price = float(item.get("price", 0))
                    stock = int(item.get("stock", 0))
                    if name:
                        self._food_repo.create(cat_id, name, desc, price, stock)
                        count += 1
                except Exception:
                    logger.warning("Skipping JSON item: %s", item)
            self._view.show_success(f"Imported {count} menu items from JSON.")
        except FileOperationError as exc:
            self._view.show_error(str(exc))

    def _export_data(self) -> None:
        while True:
            choice = self._view.show_export_submenu()
            if choice == "1":
                self._export_orders_csv()
            elif choice == "2":
                self._export_orders_json()
            elif choice == "3":
                self._export_orders_text()
            elif choice == "4":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _export_orders_csv(self) -> None:
        orders = self._order_repo.get_all()
        try:
            path = self._file_svc.get_export_path("orders.csv")
            self._file_svc.export_csv(path, orders)
            self._view.show_success(f"Orders exported to CSV: {path}")
        except FileOperationError as exc:
            self._view.show_error(str(exc))

    def _export_orders_json(self) -> None:
        orders = self._order_repo.get_all()
        try:
            path = self._file_svc.get_export_path("orders.json")
            self._file_svc.export_json(path, orders)
            self._view.show_success(f"Orders exported to JSON: {path}")
        except FileOperationError as exc:
            self._view.show_error(str(exc))

    def _export_orders_text(self) -> None:
        orders = self._order_repo.get_all()
        lines = ["IBSU Lunch Ordering System — Orders Report", "=" * 50, ""]
        for o in orders:
            lines.append(f"Order #{o['order_id']}: {o.get('student_name', 'N/A')} — K{o['total_amount']:.2f} ({o.get('status', 'N/A')})")
        content = "\n".join(lines)
        try:
            path = self._file_svc.get_export_path("orders_report.txt")
            self._file_svc.export_text_report(path, content)
            self._view.show_success(f"Orders exported to text: {path}")
        except FileOperationError as exc:
            self._view.show_error(str(exc))

    # ================================================================== #
    # USER MANAGEMENT                                                     #
    # ================================================================== #

    def _user_management(self) -> None:
        while True:
            choice = self._view.show_user_management_submenu()
            if choice == "1":
                self._view_all_users()
            elif choice == "2":
                self._delete_user()
            elif choice == "3":
                break
            else:
                self._view.show_error("Invalid choice.")

    def _view_all_users(self) -> None:
        users = self._user_repo.get_all()
        self._view.show_users_table(users)

    def _delete_user(self) -> None:
        uid = self._view.prompt_delete_user()
        if uid is None:
            return
        try:
            self._user_repo.delete(uid)
            self._view.show_success(f"User #{uid} deleted.")
        except Exception as exc:
            self._view.show_error(str(exc))
            
    def _external_service_check(self) -> None:
        """Display the current Port Moresby time from the external service."""
        try:
            result = self._external_service.get_current_time()

            self._view.show_external_service_result(result)

        except ExternalServiceError as exc:
            logger.warning("External service check failed: %s", exc)
            self._view.show_error(str(exc))
