#!/usr/bin/env python3
"""Auth class's models"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class methods"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication method"""
        if excluded_paths:
            for p in excluded_paths:
                if p[-1] == "*":
                    c = p[:-1]
                    if path:
                        if path[:len(c)] == c:
                            return False
        if path and path[-1] != '/':
            path = path + "/"
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """header authentication method"""
        if request and "Authorization" in request.headers:
            return request.headers["Authorization"]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current User authentication method"""
        return None
