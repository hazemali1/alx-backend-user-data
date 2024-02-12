#!/usr/bin/env python3
"""BasicAuth class's models"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class inherits from Auth class"""
