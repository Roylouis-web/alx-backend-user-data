#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict, TypeVar
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


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
        """
            :params
                -> email: users's email
                -> hashed_password: hashed user's password
            Returns:
                -> a User object
        """

        user = User(email=email, hashed_password=hashed_password)
        db = self._session
        db.add(user)
        db.commit()
        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """
            :params
                -> **kwargs: arbitrary keyword arguments
            Returns:
                -> a User object
        """

        db = self._session

        if not all([arg in User.__dict__ for arg in kwargs.keys()]):
            raise InvalidRequestError
        else:
            found_user = db.query(User).filter_by(**kwargs).first()
            if not found_user:
                raise NoResultFound
            return found_user

    def update_user(self, user_id: int, **kwargs: Dict):
        """
            :params
                -> user_id: user id of a user in the database
                -> kwargs: arbitrary keyword arguments
        """

        db = self._session

        if not all([arg in User.__dict__ for arg in kwargs.keys()]):
            raise ValueError

        try:
            found_user = self.find_user_by(id=user_id)
            db.query(User).filter(User.id == found_user.id).update(kwargs)
            db.commit()
        except NoResultFound:
            raise ValueError
