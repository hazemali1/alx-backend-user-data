#!/usr/bin/env python3
"""logging module"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        return(filter_datum(self.fields, self.REDACTION, super().format(record),
                            self.SEPARATOR))


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter datum fields"""
    for x in fields:
        message = re.sub(f'{x}=(.*?){separator}',
                         f'{x}={redaction}{separator}', message)
    return message
