#!/usr/bin/env python3
"""
    Module for a class called Auth
"""
from typing import TypeVar, List
from flask import request
import os


class Auth(object):
    """
        A class called Auth that contains attributes
        and methods for performing user authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            returns True if the path is not in
            the list of strings excluded_paths
        """

        if not path or not excluded_paths:
            return True
        elif path in excluded_paths or f'{path}/' in excluded_paths:
            return False
        else:
            for p in excluded_paths:
                pattern = p.split('*')
                if path.startswith(pattern[0]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            returns the value of the header request Authorization
        """

        if not request:
            return None
        elif not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns None
        """

        return None

    def session_cookie(self, request=None) -> str:
        """
            returns a cookie value from a request
        """
        SESSION_NAME = os.getenv('SESSION_NAME')
        if not request:
            return None
        return request.cookies.get(SESSION_NAME)
