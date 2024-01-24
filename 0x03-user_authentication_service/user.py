#!/usr/bin/env python3
"""
Contains a SQLAlchemy model named User for a database table named users
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model representing the 'users' table.

    Attributes:
        - id (int): The integer primary key.
        - email (str): A non-nullable string representing the user's
        email address.
        - hashed_password (str): A non-nullable string representing
        the hashed user password.
        - session_id (str): A nullable string representing the user's
        session ID.
        - reset_token (str): A nullable string representing the reset
        token for password reset.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
