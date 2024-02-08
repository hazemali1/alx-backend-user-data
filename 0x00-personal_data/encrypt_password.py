#!/usr/bin/env python3
"""Check valid and Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if password is valid"""
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
