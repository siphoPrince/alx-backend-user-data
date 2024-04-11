#!/usr/bin/env python3
"""filter_datum that returns"""


import re
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, sensitive_data=()):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.sensitive_data = sensitive_data

    def format(self, record: logging.LogRecord) -> str:
        # Compile sensitive data pattern for efficiency
        pattern = re.compile(fr"(?:"+ self.SEPARATOR + r"(?:\w+={0,1})(" + r"|".join(self.sensitive_data) + r"))=([^;]+)")
        # Apply redaction using pattern substitution
        redacted_msg = pattern.sub(rf"\1={self.REDACTION}", record.msg)
        record.msg = redacted_msg
        return super().format(record)

def filter_datum(fields, redaction, message, separator):
    pattern = r"(?:"+ separator + r"(?:\w+={0,1})(" + r"|".join(fields) + r"))=([^;]+)"
    return re.sub(pattern, rf"\1={redaction}", message)
