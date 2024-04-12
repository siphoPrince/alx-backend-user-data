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
    def __init__(self, fields):
        super().__init__()
        self.fields = set(fields)

    def format(self, record):
        for field in self.fields:
            if hasattr(record, "args") and field in record.args:
                record.args[field] = "[REDACTED]"
        return super().format(record)

def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    pii_fields = ("name", "email", "phone", "address", "credit_card")
    formatter = RedactingFormatter(pii_fields)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


PII_FIELDS = ("name", "email", "phone", "address", "credit_card")


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
    Returns the log with Regex
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


def main() -> None:
    """
    Main data from a database, formats it, and logs it with redacted PII.
    """
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
