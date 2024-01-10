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
