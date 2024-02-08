#!/usr/bin/env python3
"""logging module"""
import logging
import re
from functools import reduce


def filter_datum(fields, redaction, message, separator):
    """filter datum fields"""
    li = []
    [li.append(q[1]) for q in [re.split("=", d) for d in re.split(r';', message)] if q[0] in fields]
    message = reduce(lambda m, p: re.sub(p, redaction, m), li, message)
    return message
