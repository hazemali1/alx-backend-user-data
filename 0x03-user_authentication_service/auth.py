#!/usr/bin/env python3
"""authorization endpoint for authorization"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """uuid generator method"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user method"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """validate login method"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create session method"""
        try:
            user = self._db.find_user_by(email=email)
            session = _generate_uuid()
            user.session_id = session
            self._db._session.commit()
            return session
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from session id"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session method"""
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token from email"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except NoResultFound:
            raise ValueError
