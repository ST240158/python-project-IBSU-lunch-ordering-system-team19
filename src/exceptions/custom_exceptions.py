"""Custom exception classes for the IBSU Lunch Ordering System.

All domain-specific exceptions derive from a common base so that callers
can catch either a specific error or any application error.
"""


class IBSUAppError(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str = "An application error occurred."):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class InvalidMenuSelectionError(IBSUAppError):
    """Raised when a user enters an invalid menu option."""

    def __init__(self, selection: str = "", valid_range: tuple = (1, 1)):
        self.selection = selection
        self.valid_range = valid_range
        msg = (
            f"Invalid selection '{selection}'. "
            f"Please enter a number between {valid_range[0]} and {valid_range[1]}."
        )
        super().__init__(msg)


class InsufficientStockError(IBSUAppError):
    """Raised when an order requests more items than are available."""

    def __init__(self, item_name: str = "", requested: int = 0, available: int = 0):
        self.item_name = item_name
        self.requested = requested
        self.available = available
        msg = (
            f"Insufficient stock for '{item_name}'. "
            f"Requested: {requested}, Available: {available}."
        )
        super().__init__(msg)


class OrderNotFoundError(IBSUAppError):
    """Raised when a referenced order does not exist."""

    def __init__(self, order_id: int = 0):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} was not found.")


class InvalidCredentialsError(IBSUAppError):
    """Raised when login credentials are incorrect."""

    def __init__(self, username: str = ""):
        self.username = username
        super().__init__(f"Invalid credentials for user '{username}'.")


class DuplicateUsernameError(IBSUAppError):
    """Raised when attempting to register an already-existing username."""

    def __init__(self, username: str = ""):
        self.username = username
        super().__init__(f"Username '{username}' already exists.")


class InvalidInputError(IBSUAppError):
    """Raised when user input fails validation rules."""

    def __init__(self, field: str = "", reason: str = ""):
        self.field = field
        self.reason = reason
        super().__init__(f"Invalid input for '{field}': {reason}")


class FoodItemNotFoundError(IBSUAppError):
    """Raised when a referenced food item does not exist."""

    def __init__(self, item_id: int = 0):
        self.item_id = item_id
        super().__init__(f"Food item with ID {item_id} was not found.")


class UserNotFoundError(IBSUAppError):
    """Raised when a referenced user does not exist."""

    def __init__(self, user_id: int = 0):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} was not found.")


class OrderCannotBeCancelledError(IBSUAppError):
    """Raised when attempting to cancel an order that is past the cancellable stage."""

    def __init__(self, order_id: int = 0, status: str = ""):
        self.order_id = order_id
        self.status = status
        super().__init__(
            f"Order {order_id} cannot be cancelled because its status is '{status}'. "
            f"Only orders with status 'received' can be cancelled."
        )


class DatabaseConnectionError(IBSUAppError):
    """Raised when the database connection cannot be established."""

    def __init__(self, db_path: str = ""):
        self.db_path = db_path
        super().__init__(f"Failed to connect to database at '{db_path}'.")


class FileOperationError(IBSUAppError):
    """Raised when a file read/write operation fails."""

    def __init__(self, filepath: str = "", operation: str = "", reason: str = ""):
        self.filepath = filepath
        self.operation = operation
        self.reason = reason
        super().__init__(f"File {operation} failed for '{filepath}': {reason}")


class DuplicateCategoryError(IBSUAppError):
    """Raised when attempting to add a category that already exists."""

    def __init__(self, category_name: str = ""):
        self.category_name = category_name
        super().__init__(f"Category '{category_name}' already exists.")


class CategoryInUseError(IBSUAppError):
    """Raised when a category cannot be deleted because food items use it."""

    def __init__(self, category_id: int = 0):
        self.category_id = category_id
        super().__init__(
            f"Category with ID {category_id} cannot be deleted because it is in use by food items."
        )


class CategoryNotFoundError(IBSUAppError):
    """Raised when a referenced category does not exist."""

    def __init__(self, category_id: int = 0):
        self.category_id = category_id
        super().__init__(f"Category with ID {category_id} was not found.")


class ReportGenerationError(IBSUAppError):
    """Raised when report generation fails."""

    def __init__(self, report_type: str = "", reason: str = ""):
        self.report_type = report_type
        self.reason = reason
        super().__init__(f"Failed to generate '{report_type}' report: {reason}")


class InvalidOrderError(IBSUAppError):
    """Raised when an order is invalid (e.g. empty, no items)."""

    def __init__(self, reason: str = ""):
        self.reason = reason
        super().__init__(f"Invalid order: {reason}")
