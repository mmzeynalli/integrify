"""
Dokumentasiyalar:

AZ: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf
EN: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf
RU: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf
"""

from .env import VERSION
from .sync import EPointRequest

__all__ = ['EPointRequest', 'VERSION']
