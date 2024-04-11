#!/usr/bin/env python3
"""
This script filters personal information (PII) from log messages using regular
expressions and environmental variables.
It retrieves data from a MySQL database and logs it with redacted PII fields.
"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """
    Formatter class for redacting PII fields in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"


    def __init__(self, fields: List[str]):
         """
         nitializes the RedactingFormatter with a list of fields to redact.
         """
         self.fields = fields
         super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record by filtering values using the configured fields and redacting them.
        """
        result = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(
        self.fields,
        self.REDACTION,
        result,
        self.SEPARATOR)

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using environment variables.
    """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect

def filter_datum(fields: List[str],
         redaction: str,
         message: str,
         separator: str) -> str:
    """
    Filters a log message by replacing occurrences of PII fields with a red
    """
    for item in fields:
        message = re.sub(item + '=.*?' + separator, item + '=' +
                redaction + separator, message)
     return message

def create_user_data_logger() -> logging.Logger:
    """
    creates and configures a logger specifically for user data processing.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)
    
    return logger
