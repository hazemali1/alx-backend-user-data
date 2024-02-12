#!/usr/bin/env python3
"""Auth class's models"""
from flask import request


class Auth:
    """Auth class methods"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authentication method"""
        return False

    def authorization_header(self, request=None) -> str:
        """header authentication method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current User authentication method"""
        return None
