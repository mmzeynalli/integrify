"""
Dokumentasiya:

AZ, EN, RU: https://pg.kapitalbank.az/docs

Development and testing üçün test kartı məlumatları:
PAN: 4169741330151778, ExpDate: 11/26, CVV: 119
PAN: 5239151747183468, ExpDate: 11/24, CVV2: 292
"""

from .client import KapitalAsyncRequest, KapitalClientClass, KapitalRequest
from .env import VERSION

__all__ = ['KapitalAsyncRequest', 'KapitalClientClass', 'KapitalRequest', 'VERSION']
