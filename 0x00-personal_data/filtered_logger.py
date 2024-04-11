#!/usr/bin/env python3
"""filter_datum that returns"""


import re


import re

def filter_datum(fields, redaction, message, separator):
    pattern = r"(?:"+ separator + r"(?:\w+={0,1})(" + r"|".join(fields) + r"))=([^;]+)"
    return re.sub(pattern, rf"\1={redaction}", message)
