"""
Dokumentasiya:

EN: https://brawny-airport-7ca.notion.site/Kapital-bank-E-commerce-API-Documentation-6dd6a228c40644e3bef034bca7845e3c

Development and testing üçün test kartı məlumatları:
PAN: 4169741330151778, ExpDate: 11/26, CVV: 119
PAN: 5239151747183468, ExpDate: 11/24, CVV2: 292
"""

from .client import KapitalAsyncRequest, KapitalClientClass, KapitalRequest
from .env import VERSION

__all__ = ['KapitalAsyncRequest', 'KapitalClientClass', 'KapitalRequest', 'VERSION']
