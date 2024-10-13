from enum import Enum


class ResultCodes(str, Enum):
    SUCCESS = '00000'
    SUCCESS_GATEWAY = '00'
    SUCCESS_GATEWAY_APPROVE = 'APPROVED'
    SUCCESS_GATEWAY_PREAUTH_APPROVE = 'PREAUTH-APPROVED'
    WARNING = '01000'
    ERROR = '15000'
    INVALID_PARAMETERS = '15400'
    UNAUTHORIZED = '14010'
    TOKEN_NOT_PRESENT = '14013'
    INVALID_TOKEN = '14014'


class ResultMessages(str, Enum):
    OK = 'OK'
    SUCCESS = 'Operation performed successfully'
    ERROR = 'Internal Error'
    UNAUTHORIZED = 'Unauthorized'
    NOT_FOUND = 'Not found'

    TOKEN_NOT_PRESENT = 'Token not present'
    INVALID_TOKEN = 'Invalid Token'
    TOKEN_EXPIRED = 'Token expired'
    DEACTIVE_TOKEN = 'Token is not active'
    LINK_EXPIRED = 'Link is expired!'

    NO_RECORD_FOUND = 'No record found!'
    NO_INVOICE_FOUND = 'No invoice found!'
    APPLICATION_NOT_FOUND = 'Application not found!'
    USER_NOT_FOUND = 'User not found!'
    USER_ALREADY_EXISTS = 'User already exists!'
    UNEXPECTED_GATEWAY_ERROR = 'Occurred problem with Processing'
    INVALID_CREDENTIALS = 'Username or Password is incorrect'
