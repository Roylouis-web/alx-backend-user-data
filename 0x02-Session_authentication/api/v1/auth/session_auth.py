#!/usr/bin/env python3
"""
    A module for a class called SessionAuth
"""
from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """
        class SessionAuth that inherits from Auth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            creates a Session ID for a user_id
        """

        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id.update({
            session_id: user_id
        })
        return session_id

    def user_id_for_session_id(
            self,
            session_id: str = None) -> str:
        """
            returns a User ID based on a Session ID
        """

        if not session_id or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
             returns a User instance based on a cookie value:
        """

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return user_id

    def destroy_session(self, request=None) -> bool:
        """
            deletes the user session / logout
        """

        session_id = self.session_cookie(request)
        if not request or not self.session_cookie(request):
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True
