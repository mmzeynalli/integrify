from enum import Enum

VERSION = '2024.11.22'


class API(str, Enum):
    BASE_URL = 'https://www.sendsms.az'

    ENDPOINT = '/smxml/api'
