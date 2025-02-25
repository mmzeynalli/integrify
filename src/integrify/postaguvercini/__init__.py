"""
Dokumentasiya:

EN: https://www.poctgoyercini.com/api_json/swagger/ui/index
"""

from .client import (
    PostaGuverciniAsyncClient,
    PostaGuverciniClient,
    PostaGuverciniClientClass,
)
from .env import VERSION

__all__ = [
    'PostaGuverciniAsyncClient',
    'PostaGuverciniClientClass',
    'PostaGuverciniClient',
    'VERSION',
]
