#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user method"""
        obj = User(email=email, hashed_password=hashed_password)
        self._session.add(obj)
        self._session.commit()
        return obj

    def find_user_by(self, **kwargs):
        """find user by key and value"""
        try:
            for key, v in kwargs.items():
                k = getattr(User, key)
                result = self._session.query(User).filter(k == v).first()
            if result:
                return result
            else:
                raise NoResultFound()
        except AttributeError:
            raise InvalidRequestError()
