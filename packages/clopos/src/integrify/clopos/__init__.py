"""
Documentation:

EN: https://developer.clopos.com
"""

__path__ = __import__('pkgutil').extend_path(__path__, __name__)


from .client import CloposAsyncRequest, CloposClientClass, CloposRequest
from .env import VERSION

__all__ = ['CloposClientClass', 'CloposRequest', 'CloposAsyncRequest', 'VERSION']
