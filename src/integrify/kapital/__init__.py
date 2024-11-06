"""
Dokumentasiya:

EN: https://brawny-airport-7ca.notion.site/Kapital-bank-E-commerce-API-Documentation-6dd6a228c40644e3bef034bca7845e3c
"""

from .client import KapitalAsyncRequest, KapitalClientClass, KapitalRequest
from .env import VERSION

__all__ = ["KapitalAsyncRequest", "KapitalClientClass", "KapitalRequest", "VERSION"]
