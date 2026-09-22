"""Student (Customer) model — inherits from User and overrides abstract methods.

Demonstrates **inheritance** (extends User), **polymorphism** (overrides
abstract methods), and **composition** (holds Order references).
"""

from .user import User


class StudentCustomer(User):
    """A Student/Customer who places lunch orders.

    Attributes:
        user_id: Inherited from User.
        username: Inherited from User.
        password_hash: Inherited from User.
        name: Full display name.
        contact_info: Email or phone.
    """

    def __init__(
        self,
        user_id: int = 0,
        username: str = "",
        password_hash: str = "",
        name: str = "",
        contact_info: str = "",
    ):
        super().__init__(user_id, username, password_hash, role="student")
        self._student_id = user_id
        self._name = name.strip() if isinstance(name, str) else name
        self._contact_info = contact_info.strip() if isinstance(contact_info, str) else contact_info

    @property
    def student_id(self) -> int:
        """Return the student/customer identifier."""
        return self._student_id

    @student_id.setter
    def student_id(self, value: int) -> None:
        """Set a non-negative student/customer identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("student_id must be a non-negative integer.")
        self._student_id = value

    @property
    def name(self) -> str:
        """Return the student's display name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Return the student display name."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def contact_info(self) -> str:
        """Return contact information."""
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value: str) -> None:
        """Return the student contact information."""
        self._contact_info = value.strip()

    # ------------------------------------------------------------------ #
    # Overridden abstract methods — polymorphism                           #
    # ------------------------------------------------------------------ #

    def get_menu_options(self) -> list[str]:
        """Return student-specific menu options."""
        return [
            "View Menu",
            "Search Food",
            "Place Order",
            "View My Orders",
            "Cancel Order",
            "Logout",
        ]

    def can_manage_menu(self) -> bool:
        """Students cannot manage food items."""
        return False

    def can_update_order_status(self) -> bool:
        """Students cannot update order status."""
        return False

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return f"Student(id={self._user_id}, username='{self._username}', name='{self._name}')"

    def __repr__(self) -> str:
        return (
            f"Student(user_id={self._user_id}, username='{self._username}', "
            f"name='{self._name}', contact='{self._contact_info}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self._user_id == other._user_id

    def __hash__(self) -> int:
        return hash(self._user_id)


# Backward-compatible name retained for existing repository imports.
Student = StudentCustomer
