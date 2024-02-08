#!/usr/bin/env python3
"""Check valid and Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
