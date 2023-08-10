#!/usr/bin/env python3
"""
    Module for class named SessionExpAuth
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
        a class SessionExpAuth that inherits from SessionAuth
    """

    def __init__(self) -> None:
        """
            Initialisation
        """

        super(SessionExpAuth, self).__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
            if not self.session_duration:
                self.session_duration = 0
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
            overloads super().create_session(self, user_id=None)
        """

        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionExpAuth.user_id_by_session_id.update({
            session_id: {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        })
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
            overloads super.user_id_for_session_id(self, session_id=None)
        """

        u_id_by_session = SessionExpAuth.user_id_by_session_id
        if not session_id or session_id not in u_id_by_session.keys():
            return None
        if self.session_duration <= 0:
            user_id = u_id_by_session[session_id]["user_id"]
            return user_id
        if "created_at" not in u_id_by_session[session_id].keys():
            return None
        created_at = u_id_by_session[session_id]["created_at"]
        duration = self.session_duration
        current_time = datetime.now()
        difference = created_at + timedelta(seconds=duration)
        if difference < current_time:
            return None
        return u_id_by_session[session_id]["user_id"]
