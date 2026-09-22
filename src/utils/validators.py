"""Reusable input-validation helpers.

Every public function returns the validated, converted value or raises
``InvalidInputError`` / ``InvalidMenuSelectionError`` so that the
Controller layer can relay the message through the View.
"""

import re
from ..exceptions.custom_exceptions import InvalidInputError, InvalidMenuSelectionError


# --------------------------------------------------------------------------- #
# General input validators                                                     #
# --------------------------------------------------------------------------- #

def validate_int_input(value: str, field_name: str = "value") -> int:
    """Convert *value* to ``int`` or raise ``InvalidInputError``.

    Args:
        value: Raw string from the user.
        field_name: Human-readable label used in the error message.

    Returns:
        The converted integer.

    Raises:
        InvalidInputError: If *value* cannot be parsed as an integer.
    """
    try:
        return int(value.strip())
    except ValueError:
        raise InvalidInputError(field_name, f"'{value}' is not a valid integer.")


def validate_positive_int(value: str, field_name: str = "quantity") -> int:
    """Convert *value* to a positive ``int`` or raise ``InvalidInputError``.

    Args:
        value: Raw string from the user.
        field_name: Human-readable label used in the error message.

    Returns:
        The converted positive integer.

    Raises:
        InvalidInputError: If *value* is not a positive integer.
    """
    num = validate_int_input(value, field_name)
    if num <= 0:
        raise InvalidInputError(field_name, f"{num} is not a positive number. Please enter a value greater than 0.")
    return num


def validate_string_input(value: str, field_name: str = "input", min_length: int = 1, max_length: int = 100) -> str:
    """Validate that *value* is a non-empty string within length bounds.

    Args:
        value: Raw string from the user.
        field_name: Human-readable label used in the error message.
        min_length: Minimum acceptable length.
        max_length: Maximum acceptable length.

    Returns:
        The stripped string.

    Raises:
        InvalidInputError: If validation fails.
    """
    stripped = value.strip()
    if len(stripped) < min_length:
        raise InvalidInputError(
            field_name,
            f"Must be at least {min_length} character(s)."
        )
    if len(stripped) > max_length:
        raise InvalidInputError(
            field_name,
            f"Must not exceed {max_length} characters."
        )
    return stripped


def validate_price(value: str, field_name: str = "price") -> float:
    """Convert *value* to a positive ``float`` (2 dp) or raise ``InvalidInputError``.

    Args:
        value: Raw string from the user.
        field_name: Human-readable label used in the error message.

    Returns:
        The rounded float price.

    Raises:
        InvalidInputError: If *value* is not a valid positive price.
    """
    try:
        price = float(value.strip())
    except ValueError:
        raise InvalidInputError(field_name, f"'{value}' is not a valid number.")
    if price < 0:
        raise InvalidInputError(field_name, "Price cannot be negative.")
    return round(price, 2)


def validate_menu_selection(selection: str, min_option: int, max_option: int) -> int:
    """Validate that *selection* is an integer within [min_option, max_option].

    Args:
        selection: Raw string from the user.
        min_option: Lowest valid option number.
        max_option: Highest valid option number.

    Returns:
        The validated integer.

    Raises:
        InvalidMenuSelectionError: If out of range or non-numeric.
    """
    try:
        choice = int(selection.strip())
    except ValueError:
        raise InvalidMenuSelectionError(selection, (min_option, max_option))
    if choice < min_option or choice > max_option:
        raise InvalidMenuSelectionError(str(choice), (min_option, max_option))
    return choice


def validate_username(value: str) -> str:
    """Validate a username (3-30 alphanumeric/underscore chars, per config)."""
    from ..config import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH
    stripped = value.strip()
    if not re.match(rf"^[A-Za-z0-9_]{{{MIN_USERNAME_LENGTH},{MAX_USERNAME_LENGTH}}}$", stripped):
        raise InvalidInputError(
            "username",
            f"Must be {MIN_USERNAME_LENGTH}-{MAX_USERNAME_LENGTH} characters (letters, digits, underscores only)."
        )
    return stripped


def validate_password(value: str) -> str:
    """Validate a password (minimum 6 characters, aligned with config)."""
    from ..config import MIN_PASSWORD_LENGTH
    stripped = value.strip()
    if len(stripped) < MIN_PASSWORD_LENGTH:
        raise InvalidInputError(
            "password",
            f"Must be at least {MIN_PASSWORD_LENGTH} characters."
        )
    return stripped


def validate_name(value: str, field_name: str = "name", min_length: int = 2, max_length: int = 100) -> str:
    """Validate that *value* is a non-empty name within length bounds.

    Args:
        value: Raw string from the user.
        field_name: Human-readable label used in the error message.
        min_length: Minimum acceptable length (default 2).
        max_length: Maximum acceptable length (default 100).

    Returns:
        The stripped string if valid.

    Raises:
        InvalidInputError: If validation fails.
    """
    stripped = value.strip()
    if len(stripped) < min_length:
        raise InvalidInputError(
            field_name,
            f"Must be at least {min_length} character(s)."
        )
    if len(stripped) > max_length:
        raise InvalidInputError(
            field_name,
            f"Must not exceed {max_length} characters."
        )
    return stripped
