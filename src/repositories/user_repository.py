"""UserRepository — CRUD and authentication for the users table.

Password hashing uses SHA-256 (see note in code for production alternatives).
"""

import hashlib
import hmac
import secrets
import logging
from typing import Optional

from .database import DatabaseManager
from ..models.user import User
from ..models.student import Student
from ..models.administrator import Administrator
from ..exceptions.custom_exceptions import (
    InvalidCredentialsError,
    DuplicateUsernameError,
    UserNotFoundError,
)

logger = logging.getLogger("ibsu_lunch")


class UserRepository:
    """Data-access layer for user accounts."""

    def __init__(self, db: DatabaseManager) -> None:
        self._db = db

    @staticmethod
    def _hash_password(password: str) -> str:
        """Return a salted PBKDF2 password hash suitable for password storage."""
        salt = secrets.token_bytes(16)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
        return f"pbkdf2_sha256$310000${salt.hex()}${derived.hex()}"

    @staticmethod
    def _verify_password(password: str, stored_hash: str) -> bool:
        """Verify a password against a PBKDF2 hash."""
        try:
            algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$", 3)
            if algorithm != "pbkdf2_sha256":
                return False
            derived = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
            )
            return hmac.compare_digest(derived.hex(), digest_hex)
        except (ValueError, TypeError):
            return False

    # ------------------------------------------------------------------ #
    # Authentication                                                       #
    # ------------------------------------------------------------------ #

    def authenticate(self, username: str, password: str) -> User:
        """Verify credentials and return a User (Student or Administrator).

        Raises:
            InvalidCredentialsError: If username or password is wrong.
        """
        rows = self._db.execute_query(
            "SELECT user_id, username, password_hash, role, name, contact_info "
            "FROM users WHERE username = ?",
            (username,),
        )
        if not rows:
            raise InvalidCredentialsError("Invalid username or password.")
        row = rows[0]
        if not self._verify_password(password, row["password_hash"]):
            raise InvalidCredentialsError("Invalid username or password.")

        if row["role"] == "student":
            return Student(
                user_id=row["user_id"],
                username=row["username"],
                name=row["name"],
                contact_info=row.get("contact_info", ""),
            )
        elif row["role"] == "admin":
            return Administrator(
                user_id=row["user_id"],
                username=row["username"],
                name=row["name"],
            )
        else:
            raise InvalidCredentialsError("Unknown user role.")

    # ------------------------------------------------------------------ #
    # Create                                                               #
    # ------------------------------------------------------------------ #

    def create_student(self, username: str, password: str, name: str, contact_info: str = "") -> Student:
        """Insert a new student user and return the domain object.

        Raises:
            DuplicateUsernameError: If the username is already taken.
        """
        # Check for duplicate
        existing = self._db.execute_query(
            "SELECT user_id FROM users WHERE username = ?", (username,)
        )
        if existing:
            raise DuplicateUsernameError(username)

        pw_hash = self._hash_password(password)
        user_id = self._db.execute_insert(
            "INSERT INTO users (username, password_hash, role, name, contact_info) "
            "VALUES (?, ?, 'student', ?, ?)",
            (username, pw_hash, name, contact_info),
        )
        logger.info("Student created: id=%d, username='%s'.", user_id, username)
        return Student(user_id=user_id, username=username, name=name, contact_info=contact_info)

    def create_admin(self, username: str, password: str, name: str) -> Administrator:
        """Insert a new admin user and return the domain object.

        Raises:
            DuplicateUsernameError: If the username is already taken.
        """
        existing = self._db.execute_query(
            "SELECT user_id FROM users WHERE username = ?", (username,)
        )
        if existing:
            raise DuplicateUsernameError(username)

        pw_hash = self._hash_password(password)
        user_id = self._db.execute_insert(
            "INSERT INTO users (username, password_hash, role, name, contact_info) "
            "VALUES (?, ?, 'admin', ?, '')",
            (username, pw_hash, name),
        )
        logger.info("Admin created: id=%d, username='%s'.", user_id, username)
        return Administrator(user_id=user_id, username=username, name=name)

    # ------------------------------------------------------------------ #
    # Read                                                                 #
    # ------------------------------------------------------------------ #

    def get_by_id(self, user_id: int) -> dict | None:
        """Return a user row dict by primary key, or None."""
        rows = self._db.execute_query(
            "SELECT user_id, username, role, name, contact_info FROM users WHERE user_id = ?",
            (user_id,),
        )
        return rows[0] if rows else None

    def get_all(self) -> list[dict]:
        """Return all users as row dicts."""
        return self._db.execute_query(
            "SELECT user_id, username, role, name, contact_info FROM users ORDER BY user_id"
        )

    def get_by_role(self, role: str) -> list[dict]:
        """Return all users with a given role."""
        return self._db.execute_query(
            "SELECT user_id, username, role, name, contact_info FROM users WHERE role = ?",
            (role,),
        )

    # ------------------------------------------------------------------ #
    # Delete                                                               #
    # ------------------------------------------------------------------ #

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID. Returns True if a row was deleted."""
        count = self._db.execute_update(
            "DELETE FROM users WHERE user_id = ?", (user_id,)
        )
        if count:
            logger.info("User id=%d deleted.", user_id)
        return count > 0
