"""Administrator model — inherits from User and overrides abstract methods.

Demonstrates **inheritance** (extends User) and **polymorphism** (overrides
abstract methods with admin-specific behaviour).
"""

from .user import User


class Administrator(User):
    """A cafeteria administrator who manages food items and order status.

    Attributes:
        user_id: Inherited from User.
        username: Inherited from User.
        password_hash: Inherited from User.
        name: Full display name.
    """

    def __init__(
        self,
        user_id: int = 0,
        username: str = "",
        password_hash: str = "",
        name: str = "",
    ):
        super().__init__(user_id, username, password_hash, role="admin")
        self._admin_id = user_id
        self._name = name.strip() if isinstance(name, str) else name

    @property
    def admin_id(self) -> int:
        """Return the administrator identifier."""
        return self._admin_id

    @admin_id.setter
    def admin_id(self, value: int) -> None:
        """Set a non-negative administrator identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("admin_id must be a non-negative integer.")
        self._admin_id = value

    @property
    def name(self) -> str:
        """Return the administrator's display name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Return the administrator display name."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    # ------------------------------------------------------------------ #
    # Overridden abstract methods — polymorphism                           #
    # ------------------------------------------------------------------ #

    def get_menu_options(self) -> list[str]:
        """Return admin-specific menu options."""
        return [
            "Add Food Item",
            "View Food Items",
            "Edit Food Item",
            "Delete Food Item",
            "View Orders",
            "Update Order Status",
            "Search Orders",
            "Generate Reports",
            "Export Data",
            "Logout",
        ]

    def can_manage_menu(self) -> bool:
        """Administrators can manage food items."""
        return True

    def can_update_order_status(self) -> bool:
        """Administrators can update order status."""
        return True

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return f"Administrator(id={self._user_id}, username='{self._username}', name='{self._name}')"

    def __repr__(self) -> str:
        return (
            f"Administrator(user_id={self._user_id}, username='{self._username}', "
            f"name='{self._name}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Administrator):
            return NotImplemented
        return self._user_id == other._user_id

    def __hash__(self) -> int:
        return hash(self._user_id)
