#!/usr/bin/env python3
"""BasicAuth class's models"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """BasicAuth class inherits from Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorization header"""
        if authorization_header is None or type(authorization_header) != str \
           or authorization_header[0:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            base64.b64decode(base64_authorization_header)
        except ValueError:
            return None
        return base64.b64decode(base64_authorization_header).decode('utf-8')
