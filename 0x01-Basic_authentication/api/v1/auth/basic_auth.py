#!/usr/bin/env python3
"""
    Module for a class named BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
from models.base import DATA
from typing import TypeVar


class BasicAuth(Auth):
    """
        a class called BasicAuth that inherits from
        the Auth class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
            returns the Base64 part of the Authorization
            header for a Basic Authentication:
        """

        if not authorization_header:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
            returns the decoded value of a
            Base64 string base64_authorization_header:
            Return None if base64_authorization_header is None
        """

        if not base64_authorization_header:
            return None
        elif type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(
                    base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
            returns the user email and password from the Base64 decoded value.
        """

        a = decoded_base64_authorization_header
        result = None

        if not a:
            return (None, None)
        elif type(a) != str:
            return (None, None)
        elif len(a.split(':')) == 1:
            return (None, None)
        elif len(a.split(':')) == 2:
            result = (a.split(':')[0], a.split(':')[1])
        else:
            email = a.split(':')[0]
            password = ''
            temp = a.split(':')[1:]
            for i in range(len(temp)):
                if i < len(temp) - 1:
                    password += f'{temp[i]}:'
                elif i == len(temp) - 1 and temp[i] == '':
                    password += ':'
                else:
                    password += temp[i]
            result = (email, password)
            print(result)
        return result

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
            returns the User instance based on his email and password.
        """

        result = None
        credentials = {'email': user_email}

        if not user_email or not user_pwd or not DATA:
            return None

        for value in DATA.values():
            for v in value.values():
                if (
                    v.search(credentials) and
                    v.is_valid_password(user_pwd)
                   ):
                    result = v
        return result

    def current_user(self, request=None) -> TypeVar('User'):
        """
            overloads Auth and retrieves
            the User instance for a request
        """

        a = self.authorization_header(request)
        b = self.extract_base64_authorization_header(a)
        c = self.decode_base64_authorization_header(b)
        d = self.extract_user_credentials(c)
        if d:
            e = self.user_object_from_credentials(d[0], d[1])
        return e
