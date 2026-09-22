"""StudentView — console menus for the Student / Customer role.
"""

from tabulate import tabulate


class StudentView:
    """Renders student-facing menus and collects input."""

    DIVIDER = "=" * 60
    THIN = "-" * 60

    def show_student_menu(self, student_name: str) -> str:
        """Display the student main menu and return the choice."""
        print(self.DIVIDER)
        print(f"  STUDENT MENU — Welcome, {student_name}!")
        print(self.DIVIDER)
        print("  1. View Menu")
        print("  2. Search Food")
        print("  3. Place Order")
        print("  4. View My Orders")
        print("  5. Cancel Order")
        print("  6. Logout")
        print(self.THIN)
        return input("  Enter choice [1-6]: ").strip()

    def show_menu_table(self, items: list[dict], categories: list[dict] | None = None) -> None:
        """Display the food menu grouped by category."""
        if categories:
            for cat in categories:
                cat_items = [i for i in items if i.get("category_id") == cat["category_id"]]
                if cat_items:
                    rows = [(i["food_item_id"], i["name"], i["description"] or "", f"${i['price']:.2f}", i["stock"]) for i in cat_items]
                    print(f"\n  📂 {cat['name']}")
                    print(tabulate(rows, headers=["ID", "Name", "Description", "Price", "Stock"], tablefmt="fancy_grid"))
        else:
            rows = [(i["food_item_id"], i["name"], i["description"] or "", f"${i['price']:.2f}", i["stock"]) for i in items]
            print("\n  🍽️  Menu")
            print(tabulate(rows, headers=["ID", "Name", "Description", "Price", "Stock"], tablefmt="fancy_grid"))
        print()

    def prompt_order_items(self) -> list[dict]:
        """Collect food item selections for an order."""
        print(self.THIN)
        print("  PLACE AN ORDER")
        print("  Enter items one by one. Type 'done' to finish.")
        print(self.THIN)
        items: list[dict] = []
        while True:
            food_id = input("  Food Item ID (or 'done'): ").strip()
            if food_id.lower() == "done":
                break
            try:
                qty = int(input("  Quantity: ").strip())
                items.append({"food_item_id": int(food_id), "quantity": qty})
            except ValueError:
                print("  ❌ Invalid input. Please enter numeric ID and quantity.")
        return items

    def confirm_order(self, total: float) -> bool:
        """Ask the student to confirm the order."""
        print(f"\n  Order total: ${total:.2f}")
        choice = input("  Confirm order? (y/n): ").strip().lower()
        return choice == "y"

    def show_orders(self, orders: list[dict]) -> None:
        """Display the student's order history."""
        if not orders:
            print("\n  You have no orders yet.\n")
            return
        rows = [
            (
                o["order_id"],
                o.get("order_date", ""),
                f"${o['total_amount']:.2f}",
                o.get("status", ""),
            )
            for o in orders
        ]
        print("\n  📋 My Orders")
        print(tabulate(rows, headers=["Order ID", "Date", "Total", "Status"], tablefmt="fancy_grid"))
        print()

    def prompt_cancel_order(self) -> int | None:
        """Ask for the order ID to cancel."""
        order_id = input("  Enter Order ID to cancel (or 0 to go back): ").strip()
        try:
            oid = int(order_id)
            return oid if oid > 0 else None
        except ValueError:
            print("  ❌ Invalid Order ID.")
            return None

    def show_profile(self, student: dict) -> None:
        """Display the student's profile information."""
        print("\n  👤 My Profile")
        print(tabulate(
            [("Username", student.get("username", "")), ("Name", student.get("name", "")), ("Contact", student.get("contact_info", ""))],
            headers=["Field", "Value"],
            tablefmt="fancy_grid",
        ))
        print()

    def show_error(self, message: str) -> None:
        """Display an error message."""
        print(f"\n  ❌ Error: {message}\n")

    def show_success(self, message: str) -> None:
        """Display a success message."""
        print(f"\n  ✅ {message}\n")

    def show_info(self, message: str) -> None:
        """Display an informational message."""
        print(f"\n  ℹ️  {message}\n")
