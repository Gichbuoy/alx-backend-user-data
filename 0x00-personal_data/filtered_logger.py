#!/usr/bin/env python3
"""log message obfuscated"""
from typing import List
import re
import os
import logging
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        message = filter_datum(self.fields, self.REDACTION,
                               super(RedactingFormatter, self).format(record),
                               self.SEPARATOR)
        return message


def get_logger() -> logging.Logger:
    """
    Create and configure a logger for handling user data with
    obfuscated PII.

    Returns:
    - logging.Logger: Configured logger named "user_data" with a
    StreamHandler and RedactingFormatter.
    """
    logging.getLogger('user_data').setLevel(logging.INFO)
    logging.getLogger('user_data').propagate = False
    logging.getLogger('user_data').addHandler(logging.StreamHandler())
    logging.StreamHandler().setFormatter(RedactingFormatter(PII_FIELDS))
    return logging.getLogger('user_data')


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish a connection to the Holberton database.

    Returns:
    - mysql.connector.connection.MySQLConnection:
    Database connection object.
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connection.MySQLConnection(
        user=db_username, password=db_password, host=db_host, database=db_name)
    return connection


def main():
    """
    Retrieve all rows from the users table and display each row
    under a filtered format.

    Filtered fields:
    - name
    - email
    - phone
    - ssn
    - password
    """
    connection = get_db()
    connection.cursor().execute("SELECT * FROM users;")
    fields = [i[0] for i in connection.cursor().description]

    for row in connection.cursor():
        row_ = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        get_logger().info(row_.strip())
    connection.cursor().close()
    connection.close()
