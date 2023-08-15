#!/usr/bin/env python3
"""
    Module for a function called _hash_password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
        :params
            -> password: user password to be hashed
        Returns:
            -> password converted to bytes
    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
        generates a uuid to be used a session_id
    """
    return str(uuid.uuid4())


class Auth:
    """
        Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            :params
                -> email: user's email
                -> password: user's password
            Returns:
                -> a User object
        """

        try:
            found_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {found_user.email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
            :params
                -> email: user's email
                -> password: user's password
            Returns:
                -> a boolean
        """

        try:
            found_user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  found_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
            :params
                -> email: user's email
            Returns:
                -> the users's session id
        """

        try:
            found_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(found_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
            :params
                -> session_id: the user's session id
        """

        if not session_id:
            return None
        try:
            found_user = self._db.find_user_by(session_id=session_id)
            return found_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
            :params
                -> user_id: the user's id
        """

        try:
            found_user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
            :params
                -> email: the current user's email
            Returns:
                -> a uuid
        """

        try:
            found_user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(found_user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
            :params
                -> password: the user's password
        """

        try:
            found_user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(found_user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
