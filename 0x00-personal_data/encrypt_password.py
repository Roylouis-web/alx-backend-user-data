#!/usr/bin/env python3
'''
    Module for a function named hashed_password
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
        returns a hashed_password
    '''

    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
        validates a password
    '''

    return bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
