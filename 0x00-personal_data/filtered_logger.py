#!/usr/bin/env python3
'''
    Module for a function named filtered_datum
'''

from typing import List
import re
import logging
import mysql.connector
import os
import bcrypt


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    '''A function that returns the log message obufuscated'''
    for field in fields:
        message = re.sub(r'{}=.+?(?={})'.format(field, separator),
                         '{}={}'.format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = re.sub(';', '; ',
                     filter_datum(self.fields, self.REDACTION,
                                  record.__dict__['msg'], self.SEPARATOR))
        record.__dict__['asctime'] = self.formatTime(record)
        record.__dict__['message'] = msg
        return self.FORMAT % record.__dict__


def get_logger() -> logging.Logger:
    '''
        returns a logging.Logger object
    '''

    logger = logging.Logger('user_data', logging.INFO)
    logger.__dict__['propagate'] = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter)
    logger.__dict__['handlers'].append(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
        returns a connector to mysql database
    '''

    return mysql.connector.connection.MySQLConnection(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database='PERSONAL_DATA_DB_NAME')


PII_FIELDS = ['ssn', 'email', 'phone', 'password', 'ip']
