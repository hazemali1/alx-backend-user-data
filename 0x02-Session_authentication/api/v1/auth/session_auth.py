#!/usr/bin/env python3
"""Auth class's models"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """session auth class"""
