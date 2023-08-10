#!/usr/bin/env python3
"""
    Module for a class named SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import json
from datetime import datetime, timedelta
import os


class SessionDBAuth(SessionExpAuth):
    """
        a class SessionDBAuth that inherits from SessionExpAuth
    """

    def create_session(self, user_id=None) -> str:
        """
            creates and stores new instance of
            UserSession and returns the Session ID
        """

        if not user_id or type(user_id) != str:
            return None

        session_id = super().create_session(user_id)

        if not session_id:
            return None

        credentials = {'user_id': user_id, 'session_id': session_id}
        user = UserSession(**credentials)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
            returns the User ID by requesting
            UserSession in the database based on session_id
        """
        from models.base import DATA

        UserSession.load_from_file()
        seconds = None

        try:
            seconds = int(os.getenv('SESSION_DURATION'))
            if not seconds:
                seconds = 0
        except Exception:
            seconds = 0

        if not session_id:
            return None
        temp = DATA.get(UserSession.__name__)
        user = None
        if temp:
            for values in temp.values():
                if values.session_id == session_id:
                    user = values
            if not user:
                return None
            if not user.session_id:
                return None
            if user.session_id != session_id:
                return None
            if seconds <= 0:
                return user.user_id
            if not user.__dict__.get('created_at'):
                return None
            if not user.__dict__.get('session_id'):
                return None
            current_time = datetime.now()
            created_at = user.created_at
            difference = created_at + timedelta(seconds=seconds)
            if difference < current_time:
                return None
            return user.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """
            destroys the UserSession based
            on the Session ID from the request cookie
        """
        from models.base import DATA

        UserSession.load_from_file()

        temp = DATA.get(UserSession.__name__)
        session_id = super().session_cookie(request)
        user = None
        if not request:
            return False
        if not session_id:
            return False
        if temp:
            for values in temp.values():
                if values.session_id == session_id:
                    user = values
            if not user:
                return False
            user.remove()
        return True
