"""
Dokumentasiyalar:

AZ: https://developer.azericard.com/az
EN: https://developer.azericard.com/en


Development and testing üçün test kartı məlumatları:
PAN: 4127211288596748, ExpDate: 10/27, CVV: 931 SMS OTP: 1111
PAN: 5167513336327283, ExpDate: 10/27, CVV: 209 SMS OTP: 1111
"""

from .client import AzeriCardAsyncClient, AzeriCardClient, AzeriCardClientClass
from .env import VERSION

__all__ = ['AzeriCardAsyncClient', 'AzeriCardClientClass', 'AzeriCardClient', 'VERSION']
