"""User base class — demonstrates inheritance, encapsulation, and abstract methods.

Both ``Student`` and ``Administrator`` inherit from this class, sharing
authentication attributes while overriding role-specific behaviour.
"""

from abc import ABC, abstractmethod


class User(ABC):
    """Abstract base class for all system users.

    Attributes:
        user_id: Primary key from the database (0 before persistence).
        username: Unique login identifier.
        password_hash: Hashed password string.
        role: Either ``'student'`` or ``'admin'``.
    """

    def __init__(
        self,
        user_id: int = 0,
        username: str = "",
        password_hash: str = "",
        role: str = "",
    ):
        self._user_id = user_id
        self._username = username
        self._password_hash = password_hash
        self._role = role

    # ------------------------------------------------------------------ #
    # Properties — controlled attribute access                              #
    # ------------------------------------------------------------------ #

    @property
    def user_id(self) -> int:
        """Return the user's database ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Return the user database identifier."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("user_id must be a non-negative integer.")
        self._user_id = value

    @property
    def username(self) -> str:
        """Return the username."""
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        """Return the username."""
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters.")
        self._username = value.strip()

    @property
    def password_hash(self) -> str:
        """Return the hashed password (write-only from outside)."""
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value: str) -> None:
        """Return the stored password hash."""
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Password hash cannot be empty.")
        self._password_hash = value

    @property
    def role(self) -> str:
        """Return the user's role."""
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        """Return the user role."""
        if value not in ("student", "admin"):
            raise ValueError("Role must be 'student' or 'admin'.")
        self._role = value

    # ------------------------------------------------------------------ #
    # Abstract methods — polymorphism / method overriding                   #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def get_menu_options(self) -> list[str]:
        """Return the list of menu options available to this user role."""
        ...

    @abstractmethod
    def can_manage_menu(self) -> bool:
        """Return True if the user can add/edit/delete food items."""
        ...

    @abstractmethod
    def can_update_order_status(self) -> bool:
        """Return True if the user can change order status."""
        ...

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:
        return f"User(id={self._user_id}, username='{self._username}', role='{self._role}')"

    def __repr__(self) -> str:
        return f"User(user_id={self._user_id}, username='{self._username}', role='{self._role}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self._user_id == other._user_id

    def __hash__(self) -> int:
        return hash(self._user_id)
