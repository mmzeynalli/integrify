from enum import Enum


class ResultCodes(str, Enum):
    SUCCESS = '00000'
    SUCCESS_GATEWAY = '00'
    SUCCESS_GATEWAY_APPROVE = 'APPROVED'
    SUCCESS_GATEWAY_PREAUTH_APPROVE = 'PREAUTH-APPROVED'
    WARNING = '01000'
    ERROR = '15000'
    INVALID_PARAMETERS = '15400'
    UNAUTHORIZED = '14010'  # nosec: B105
    TOKEN_NOT_PRESENT = '14013'  # nosec: B105
    INVALID_TOKEN = '14014'  # nosec: B105


class ResultMessages(str, Enum):
    OK = 'OK'
    SUCCESS = 'Operation performed successfully'
    ERROR = 'Internal Error'
    UNAUTHORIZED = 'Unauthorized'
    NOT_FOUND = 'Not found'

    TOKEN_NOT_PRESENT = 'Token not present'  # nosec: B105
    INVALID_TOKEN = 'Invalid Token'  # nosec: B105
    TOKEN_EXPIRED = 'Token expired'  # nosec: B105
    DEACTIVE_TOKEN = 'Token is not active'  # nosec: B105
    LINK_EXPIRED = 'Link is expired!'  # nosec: B105

    NO_RECORD_FOUND = 'No record found!'
    NO_INVOICE_FOUND = 'No invoice found!'
    APPLICATION_NOT_FOUND = 'Application not found!'
    USER_NOT_FOUND = 'User not found!'
    USER_ALREADY_EXISTS = 'User already exists!'
    UNEXPECTED_GATEWAY_ERROR = 'Occurred problem with Processing'
    INVALID_CREDENTIALS = 'Username or Password is incorrect'


class Currency(str, Enum):
    AZN = 'AZN'
    USD = 'USD'
    EUR = 'EUR'


class Operation(str, Enum):
    PURCHASE = 'PURCHASE'
    PRE_AUTH = 'PRE_AUTH'


class Language(str, Enum):
    AZ = 'AZ'
    EN = 'EN'
    RU = 'RU'
