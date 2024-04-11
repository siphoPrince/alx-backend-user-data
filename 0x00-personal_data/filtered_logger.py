#!/usr/bin/env python3
"""
Filter personal information using a Regex, Environmental variables, etc.
"""

import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.
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
    Connect to mysql server with environmental vars
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
    Returns the log message obfuscated with Regex
    """
    for item in fields:
        message = re.sub(item + '=.*?' + separator, item + '=' +
                         redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a Logger object with a
    StreamHandler with RedactingFormatter
    as formatter
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
    Obtain a database connection using get_db
    and retrieve all rows in the users table and display each row w/ format:

    [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596:
    name=***; email=***; phone=***; ssn=***; password=***;
    ip=60ed:c396:2ff:244:bbd0:9208:26f2:93ea; last_login=2019-11-14 06:14:24
    user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36;
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
