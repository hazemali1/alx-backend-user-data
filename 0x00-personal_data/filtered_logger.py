#!/usr/bin/env python3
"""logging module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter datum fields"""
    for x in fields:
        message = re.sub(f'{x}=(.*?){separator}',
                         f'{x}={redaction}{separator}', message)
    return message
