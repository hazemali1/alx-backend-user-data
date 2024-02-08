#!/usr/bin/env python3
"""logging module"""
import logging
import re
from functools import reduce
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter datum fields"""
    li = []
    [li.append(q[1]) for q in [re.split("=", d) for d in re.split(r';', message)] if q[0] in fields]
    message = reduce(lambda m, p: re.sub(p, redaction, m), li, message)
    return message
