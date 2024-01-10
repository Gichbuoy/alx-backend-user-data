#!/usr/bin/env python3
"""
Encrypting password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with a salt.

    Args:
    - password (str): The plaintext password to be hashed.

    Returns:
    - bytes: The salted and hashed password as a byte string.
    """
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password
    using bcrypt.

    Args:
    - hashed_password (bytes): The salted and hashed password.
    - password (str): The plaintext password to be validated.

    Returns:
    - bool: True if the password is valid, False otherwise.
    """
    if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
        return True
    return False
