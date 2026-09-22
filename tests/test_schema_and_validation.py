"""Regression tests for the reproducible SQL script and input validators."""

import hashlib
import sqlite3
from pathlib import Path

import pytest

from src.exceptions.custom_exceptions import InvalidInputError, InvalidMenuSelectionError
from src.utils.validators import (
    validate_int_input,
    validate_positive_int,
    validate_price,
    validate_username,
    validate_password,
    validate_name,
    validate_menu_selection,
)


def test_schema_sql_recreates_application_database():
    """The standalone SQL deliverable must match the application's schema."""
    sql = Path("database/schema.sql").read_text(encoding="utf-8")
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(sql)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert {"users", "category", "food_items", "orders", "order_items", "order_status"} <= tables

    user_columns = {
        row[1] for row in connection.execute("PRAGMA table_info(users)")
    }
    assert {"password_hash", "role", "contact_info"} <= user_columns

    student_hash = connection.execute(
        "SELECT password_hash FROM users WHERE username = 'student'"
    ).fetchone()[0]
    assert student_hash.startswith("pbkdf2_sha256$310000$")
    assert connection.execute("SELECT COUNT(*) FROM food_items").fetchone()[0] == 12

    connection.close()


def test_validators_accept_expected_values():
    """Happy-path validator inputs should be normalised and converted."""
    assert validate_int_input(" 12 ") == 12
    assert validate_positive_int("3") == 3
    assert validate_price("7.456") == 7.46
    assert validate_username("student_01") == "student_01"
    assert validate_password("secret1") == "secret1"
    assert validate_name("  Alice Smith  ") == "Alice Smith"
    assert validate_menu_selection("2", 1, 4) == 2


@pytest.mark.parametrize("value", ["", "ab", "bad-name", "has space"])
def test_invalid_usernames_are_rejected(value):
    """Invalid usernames should raise the domain validation exception."""
    with pytest.raises(InvalidInputError):
        validate_username(value)


def test_invalid_positive_integer_is_rejected():
    """Zero is not a valid positive quantity."""
    with pytest.raises(InvalidInputError):
        validate_positive_int("0")


def test_invalid_price_is_rejected():
    """Negative prices are not allowed."""
    with pytest.raises(InvalidInputError):
        validate_price("-1")


def test_invalid_menu_selection_is_rejected():
    """Menu choices outside the allowed range should raise a custom error."""
    with pytest.raises(InvalidMenuSelectionError):
        validate_menu_selection("9", 1, 4)


def test_json_configuration_selects_sqlite_backend():
    import json
    from pathlib import Path
    from src.repositories.database import DatabaseManager
    config = json.loads(Path("config.json").read_text(encoding="utf-8"))
    db = DatabaseManager.from_config(config)
    assert db.backend == "sqlite"
    db.close()
