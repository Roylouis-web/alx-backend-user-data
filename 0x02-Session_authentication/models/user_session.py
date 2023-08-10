#!/usr/bin/env python3
"""
    Module for a class named UserSession
"""
from models.base import Base


class UserSession(Base):
    """
        a class UserSession that inherits from Base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
            Initialises the class
        """

        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
