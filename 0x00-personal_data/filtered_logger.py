#!/usr/bin/env python3
"""logging module"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter datum fields"""
    for x in fields:
        message = re.sub(f'{x}=(.*?){separator}',
                         f'{x}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initial constructor for RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Return a string representation of the record"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "phone", "ssn")


def get_logger() -> logging.Logger:
    """ Return a logger """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    log.addHandler(h)
    return log
