"""
Dokumentasiya:

EN: https://www.poctgoyercini.com/api_json/swagger/ui/index
"""

from .client import (
    PostaGuverciniAsyncRequest,
    PostaGuverciniClientClass,
    PostaGuverciniRequest,
)
from .env import VERSION

__all__ = [
    'PostaGuverciniAsyncRequest',
    'PostaGuverciniClientClass',
    'PostaGuverciniRequest',
    'VERSION',
]
