#!/usr/bin/env python3
"""BasicAuth class's models"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        s = decoded_base64_authorization_header.split(":")
        return (s[0], s[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """user object from credentials"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        obj = User()
        if len(obj.search({'email': user_email})) == 0:
            return None
        if obj.search({'email': user_email})[0].is_valid_password(user_pwd):
            return obj.search({'email': user_email})[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """curren user overloads"""
        a_h = self.authorization_header(request)
        if a_h:
            e_b_a_h = self.extract_base64_authorization_header(a_h)
            if e_b_a_h:
                d_b_a_h = self.decode_base64_authorization_header(e_b_a_h)
                if d_b_a_h:
                    e_u_c = self.extract_user_credentials(d_b_a_h)
                    if e_u_c:
                        t = e_u_c
                        u_o_f_c = self.user_object_from_credentials(t[0], t[1])
                        return u_o_f_c
        return None
