#!/usr/bin/env python3
"""
User authentication module
"""

import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> str:
    """
    Hash the input password using bcrypt with a randomly generated salt.

    Args:
        password (str): The input password to be hashed.

    Returns:
        bytes: The salted hash of the input password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The User object representing the registered user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            user = None
        if user:
            raise ValueError('User {} already exist'.format(email))
        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password entered by the user.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID and return its string representation.

        Returns:
            str: String representation of the new UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session ID for user and return it"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user based on their session ID"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
            except Exception:
                return None
            return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session ID"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a password reset token"""
        try:
            user = self._db.find_user_by(email=email)
        except UserNotFoundError:
            raise ValueError("User DNE")
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password if reset tooken is available in db"""
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            user = None
        if user is not None:
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_password,
                reset_token=None
            )
        raise ValueError
