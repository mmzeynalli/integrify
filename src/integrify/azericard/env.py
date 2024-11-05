import os
from enum import Enum
from typing import Literal

AZERICARD_MERCHANT_ID = os.getenv('AZERICARD_MERCHANT_ID', '')


class API(str, Enum):
    """Endpoint constant-ları"""

    AUTHORIZATION: Literal['/cgi-bin/cgi_link'] = '/cgi-bin/cgi_link'
    SAVE_CARD: Literal['/token/cgi_link'] = '/token/cgi_link'


__all__ = [
    'AZERICARD_MERCHANT_ID',
    'API',
]
