"""AuthService — wraps authentication and registration logic.

Delegates database work to ``UserRepository`` and provides a clean API
for the Controller layer.
"""

import logging
from ..repositories.user_repository import UserRepository
from ..models.user import User
from ..exceptions.custom_exceptions import InvalidCredentialsError, DuplicateUsernameError

logger = logging.getLogger("ibsu_lunch")


class AuthService:
    """Handles user authentication and account registration."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def login(self, username: str, password: str) -> User:
        """Authenticate a user and return the domain object.

        Args:
            username: Login username.
            password: Plain-text password.

        Returns:
            A ``Student`` or ``Administrator`` instance.

        Raises:
            InvalidCredentialsError: If credentials are invalid.
        """
        try:
            user = self._user_repo.authenticate(username, password)
            logger.info("User '%s' logged in (role=%s).", username, user.role)
            return user
        except InvalidCredentialsError:
            logger.warning("Failed login attempt for username '%s'.", username)
            raise

    def register_student(
        self, username: str, password: str, name: str, contact_info: str = ""
    ) -> User:
        """Register a new student/customer account.

        Raises:
            DuplicateUsernameError: If the username is already taken.
        """
        try:
            student = self._user_repo.create_student(username, password, name, contact_info)
            logger.info("New student registered: '%s' (id=%s).", username, student.user_id)
            return student
        except DuplicateUsernameError:
            logger.warning("Registration failed — duplicate username: '%s'.", username)
            raise

    def register_admin(self, username: str, password: str, name: str) -> User:
        """Register a new administrator account.

        Raises:
            DuplicateUsernameError: If the username is already taken.
        """
        try:
            admin = self._user_repo.create_admin(username, password, name)
            logger.info("New admin registered: '%s' (id=%s).", username, admin.user_id)
            return admin
        except DuplicateUsernameError:
            logger.warning("Registration failed — duplicate username: '%s'.", username)
            raise
