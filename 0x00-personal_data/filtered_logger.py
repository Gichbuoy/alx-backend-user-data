#!/usr/bin/env python3
"""log message obfuscated"""
from typing import List
import re
import os
import logging
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message using redaction.

    Args:
    - fields (list): List of strings representing fields to obfuscate.
    - redaction (str): String representing the redaction value.
    - message (str): String representing the log line.
    - separator (str): String representing the character separating
    fields in the log line.

    Returns:
    - str: Log message with specified fields obfuscated.
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message
