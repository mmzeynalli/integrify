"""
Dokumentasiyalar:

AZ: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf
EN: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf
RU: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf
"""

from .client import EPointAsyncRequest, EPointRequest
from .env import VERSION

__all__ = ['EPointRequest', 'EPointAsyncRequest', 'VERSION']
