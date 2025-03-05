"""
Dokumentasiya: https://docs.payriff.com/

Test kard məlumatları:

VISA:
    Cardholder: Test Test
    number: 4000007546012078
    exp: 04/29
    CVV: 893

MC:
    Cardholder: Test Test
    number: 5000005541096514
    exp: 08/28
    CVV: 587

OTP: 123456
"""

from .client import PayriffAsyncClient, PayriffClient, PayriffClientClass

__all__ = ['PayriffClientClass', 'PayriffClient', 'PayriffAsyncClient']
