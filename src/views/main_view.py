"""MainView — top-level console menus (login / role routing).
"""

from tabulate import tabulate


class MainView:
    """Renders the main application menus and collects user input."""

    DIVIDER = "=" * 60
    THIN = "-" * 60

    def show_banner(self) -> None:
        """Display the application welcome banner."""
        print()
        print(self.DIVIDER)
        print("   IBSU LUNCH ORDERING SYSTEM")
        print("   Intitute Of Bussiness Studies University — Campus Cafeteria")
        print(self.DIVIDER)
        print()

    def show_main_menu(self) -> str:
        """Show the main menu and return the user's choice."""
        print(self.DIVIDER)
        print("  MAIN MENU")
        print(self.DIVIDER)
        print("  1. Student Login")
        print("  2. Administrator Login")
        print("  3. Exit")
        print(self.THIN)
        return input("  Enter choice [1-3]: ").strip()

    def prompt_login(self) -> tuple[str, str]:
        """Collect username and password."""
        print(self.THIN)
        print("  LOGIN")
        print(self.THIN)
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()
        return username, password

    def show_error(self, message: str) -> None:
        """Display an error message."""
        print(f"\n  ❌ Error: {message}\n")

    def show_success(self, message: str) -> None:
        """Display a success message."""
        print(f"\n  ✅ {message}\n")

    def show_info(self, message: str) -> None:
        """Display an informational message."""
        print(f"\n  ℹ️  {message}\n")

    def show_goodbye(self) -> None:
        """Display the exit message."""
        print()
        print(self.DIVIDER)
        print("  Thank you for using the IBSU Lunch Ordering System!")
        print("  Goodbye!")
        print(self.DIVIDER)
        print()

    def show_table(self, data: list, headers: list, title: str = "") -> None:
        """Render a list of rows as a formatted table via tabulate."""
        if title:
            print(f"\n  {title}")
        if not data:
            print("  (No data to display.)\n")
            return
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        print()
