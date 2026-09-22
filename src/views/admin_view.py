"""AdminView — console menus for the Administrator role.
"""

from tabulate import tabulate


class AdminView:
    """Renders admin-facing menus and collects input."""

    DIVIDER = "=" * 60
    THIN = "-" * 60

    def show_admin_menu(self, admin_name: str) -> str:
        """Display the admin main menu and return the choice."""
        print(self.DIVIDER)
        print(f"  ADMIN MENU — Welcome, {admin_name}!")
        print(self.DIVIDER)
        print("  1. Add Food Item")
        print("  2. View Food Items")
        print("  3. Edit Food Item")
        print("  4. Delete Food Item")
        print("  5. View Orders")
        print("  6. Update Order Status")
        print("  7. Generate Reports")
        print("  8. Logout")
        print(self.THIN)
        return input("  Enter choice [1-8]: ").strip()

    # ------------------------------------------------------------------ #
    # Menu Item management                                                #
    # ------------------------------------------------------------------ #

    def show_menu_item_submenu(self) -> str:
        """Display the menu-item management submenu and return the selected option."""
        print(self.THIN)
        print("  MENU ITEM MANAGEMENT")
        print(self.THIN)
        print("  1. Add Menu Item")
        print("  2. Update Menu Item")
        print("  3. Delete Menu Item")
        print("  4. View All Menu Items")
        print("  5. Search Menu Items")
        print("  6. Back")
        return input("  Enter choice [1-6]: ").strip()

    def prompt_add_menu_item(self, categories: list[dict]) -> dict:
        """Collect details for a new menu item."""
        print(self.THIN)
        print("  ADD MENU ITEM")
        cat_rows = [(c["category_id"], c["name"]) for c in categories]
        print(tabulate(cat_rows, headers=["Category ID", "Name"], tablefmt="fancy_grid"))
        cat_id = int(input("  Category ID: ").strip())
        name = input("  Item name: ").strip()
        desc = input("  Description: ").strip()
        price = float(input("  Price: ").strip())
        stock = int(input("  Initial stock: ").strip())
        return {"category_id": cat_id, "name": name, "description": desc, "price": price, "stock": stock}

    def prompt_update_menu_item(self, items: list[dict]) -> dict | None:
        """Collect fields to update for an existing menu item."""
        if not items:
            self.show_info("No menu items found.")
            return None
        self.show_food_items_table(items)
        item_id = input("  Enter Food Item ID to update (or 0 to cancel): ").strip()
        if item_id == "0":
            return None
        print("  Leave field blank to keep current value.")
        name = input("  New name: ").strip() or None
        desc = input("  New description: ").strip() or None
        price = input("  New price: ").strip()
        price = float(price) if price else None
        stock = input("  New stock: ").strip()
        stock = int(stock) if stock else None
        cat_id = input("  New category ID: ").strip()
        cat_id = int(cat_id) if cat_id else None
        return {"food_item_id": int(item_id), "name": name, "description": desc, "price": price, "stock": stock, "category_id": cat_id}

    def prompt_delete_menu_item(self) -> int | None:
        """Collect the menu-item identifier to delete."""
        item_id = input("  Enter Food Item ID to delete (or 0 to cancel): ").strip()
        try:
            iid = int(item_id)
            return iid if iid > 0 else None
        except ValueError:
            self.show_error("Invalid ID.")
            return None

    def show_food_items_table(self, items: list[dict], title: str = "🍽️  Menu Items") -> None:
        """Render food items in a formatted console table."""
        if not items:
            print(f"\n  {title}\n  (No items to display.)\n")
            return
        rows = [(i["food_item_id"], i["category_id"], i["name"], i.get("description", ""), f"${i['price']:.2f}", i["stock"]) for i in items]
        print(f"\n  {title}")
        print(tabulate(rows, headers=["ID", "Cat ID", "Name", "Description", "Price", "Stock"], tablefmt="fancy_grid"))
        print()

    def prompt_search(self) -> str:
        """Collect search criteria for order or menu-item filtering."""
        return input("  Search keyword: ").strip()

    # ------------------------------------------------------------------ #
    # Category management                                                  #
    # ------------------------------------------------------------------ #

    def show_category_submenu(self) -> str:
        """Display category-management options."""
        print(self.THIN)
        print("  CATEGORY MANAGEMENT")
        print(self.THIN)
        print("  1. Add Category")
        print("  2. Update Category")
        print("  3. Delete Category")
        print("  4. View All Categories")
        print("  5. Back")
        return input("  Enter choice [1-5]: ").strip()

    def prompt_add_category(self) -> dict:
        """Collect details for a new category."""
        print(self.THIN)
        print("  ADD CATEGORY")
        name = input("  Category name: ").strip()
        desc = input("  Description: ").strip()
        return {"name": name, "description": desc}

    def prompt_update_category(self, categories: list[dict]) -> dict | None:
        """Collect fields to update for a category."""
        if not categories:
            self.show_info("No categories found.")
            return None
        self.show_categories_table(categories)
        cat_id = input("  Enter Category ID to update (or 0 to cancel): ").strip()
        if cat_id == "0":
            return None
        print("  Leave blank to keep current value.")
        name = input("  New name: ").strip() or None
        desc = input("  New description: ").strip() or None
        return {"category_id": int(cat_id), "name": name, "description": desc}

    def prompt_delete_category(self) -> int | None:
        """Collect the category identifier to delete."""
        cat_id = input("  Enter Category ID to delete (or 0 to cancel): ").strip()
        try:
            cid = int(cat_id)
            return cid if cid > 0 else None
        except ValueError:
            self.show_error("Invalid ID.")
            return None

    def show_categories_table(self, categories: list[dict]) -> None:
        """Render categories in a formatted table."""
        if not categories:
            print("\n  (No categories to display.)\n")
            return
        rows = [(c["category_id"], c["name"], c.get("description", "")) for c in categories]
        print("\n  📂 Categories")
        print(tabulate(rows, headers=["ID", "Name", "Description"], tablefmt="fancy_grid"))
        print()

    # ------------------------------------------------------------------ #
    # Order management                                                     #
    # ------------------------------------------------------------------ #

    def show_orders_table(self, orders: list[dict], title: str = "📋 All Orders") -> None:
        """Render orders in a formatted table."""
        if not orders:
            print(f"\n  {title}\n  (No orders to display.)\n")
            return
        rows = [
            (o["order_id"], o.get("student_name", ""), o.get("order_date", ""), f"${o['total_amount']:.2f}", o.get("status", ""))
            for o in orders
        ]
        print(f"\n  {title}")
        print(tabulate(rows, headers=["Order ID", "Student", "Date", "Total", "Status"], tablefmt="fancy_grid"))
        print()

    def prompt_update_order_status(self) -> tuple[int, int] | None:
        """Collect an order ID and target status."""
        order_id = input("  Enter Order ID: ").strip()
        print("  Available statuses: 1=received, 2=preparing, 3=ready, 4=collected")
        status_id = input("  New Status ID: ").strip()
        try:
            return int(order_id), int(status_id)
        except ValueError:
            self.show_error("Invalid Order ID or Status ID.")
            return None

    def prompt_delete_order(self) -> int | None:
        """Collect an order ID for administrative deletion."""
        order_id = input("  Enter Order ID to delete (or 0 to cancel): ").strip()
        try:
            value = int(order_id)
            return value if value > 0 else None
        except ValueError:
            self.show_error("Invalid Order ID.")
            return None

    # ------------------------------------------------------------------ #
    # Reports                                                              #
    # ------------------------------------------------------------------ #

    def show_report_submenu(self) -> str:
        """Display report-management options."""
        print(self.THIN)
        print("  REPORTS")
        print(self.THIN)
        print("  1. Daily Sales Report")
        print("  2. Popular Items Report")
        print("  3. Category Revenue Report")
        print("  4. Generate Charts")
        print("  5. Export Full Report (TXT/CSV/JSON)")
        print("  6. Back")
        return input("  Enter choice [1-6]: ").strip()

    def prompt_report_date(self) -> str:
        """Collect an optional report date."""
        return input("  Enter date (YYYY-MM-DD, or leave blank for today): ").strip()

    def show_dataframe(self, df, title: str = "Report") -> None:
        """Display a pandas DataFrame using tabulate."""
        if df.empty:
            print(f"\n  {title}\n  (No data.)\n")
            return
        print(f"\n  {title}")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        print()

    def show_chart_paths(self, paths: dict[str, str]) -> None:
        """Display the paths of generated chart images."""
        if not paths:
            self.show_info("No charts were generated.")
            return
        print("\n  📊 Charts saved:")
        for label, path in paths.items():
            print(f"    {label}: {path}")
        print()

    # ------------------------------------------------------------------ #
    # Import / Export                                                      #
    # ------------------------------------------------------------------ #

    def show_import_submenu(self) -> str:
        """Display CSV/JSON import options."""
        print(self.THIN)
        print("  IMPORT MENU FROM FILE")
        print(self.THIN)
        print("  1. Import from CSV")
        print("  2. Import from JSON")
        print("  3. Back")
        return input("  Enter choice [1-3]: ").strip()

    def prompt_import_filename(self, fmt: str) -> str:
        """Collect an import filename."""
        return input(f"  Enter {fmt.upper()} filename (in data/imports/): ").strip()

    def show_export_submenu(self) -> str:
        """Display data-export options."""
        print(self.THIN)
        print("  EXPORT DATA")
        print(self.THIN)
        print("  1. Export Orders to CSV")
        print("  2. Export Orders to JSON")
        print("  3. Export Orders to Text Report")
        print("  4. Back")
        return input("  Enter choice [1-4]: ").strip()

    # ------------------------------------------------------------------ #
    # User management                                                      #
    # ------------------------------------------------------------------ #

    def show_user_management_submenu(self) -> str:
        """Display user-management options."""
        print(self.THIN)
        print("  USER MANAGEMENT")
        print(self.THIN)
        print("  1. View All Users")
        print("  2. Delete a User")
        print("  3. Back")
        return input("  Enter choice [1-3]: ").strip()

    def show_users_table(self, users: list[dict]) -> None:
        """Render users in a formatted table."""
        if not users:
            print("\n  (No users to display.)\n")
            return
        rows = [(u["user_id"], u["username"], u["name"], u["role"]) for u in users]
        print("\n  👥 Users")
        print(tabulate(rows, headers=["ID", "Username", "Name", "Role"], tablefmt="fancy_grid"))
        print()

    def prompt_delete_user(self) -> int | None:
        """Collect the user identifier to delete."""
        uid = input("  Enter User ID to delete (or 0 to cancel): ").strip()
        try:
            val = int(uid)
            return val if val > 0 else None
        except ValueError:
            self.show_error("Invalid ID.")
            return None

    # ------------------------------------------------------------------ #
    # Shared helpers                                                       #
    # ------------------------------------------------------------------ #

    def show_error(self, message: str) -> None:
        """Display an error message."""
        print(f"\n  ❌ Error: {message}\n")

    def show_success(self, message: str) -> None:
        """Display a success message."""
        print(f"\n  ✅ {message}\n")

    def show_info(self, message: str) -> None:
        """Display an informational message."""
        print(f"\n  ℹ️  {message}\n")
