"""
Package to use EPoint endpoints. You need to set EPOINT_PUBLIC_KEY and EPOINT_PRIVATE_KEY
environmental variables to be able to use this package. For documentation, refer to:

AZ: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf
EN: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf
RU: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf
"""

import os
from warnings import warn

from dotenv import load_dotenv

load_dotenv()

EPOINT_PUBLIC_KEY: str = os.getenv('EPOINT_PUBLIC_KEY', '')
EPOINT_PRIVATE_KEY: str = os.getenv('EPOINT_PRIVATE_KEY', '')

EPOINT_SUCCESS_REDIRECT_URL: str | None = os.getenv('EPOINT_SUCCESS_REDIRECT_URL')
EPOINT_FAILED_REDIRECT_URL: str | None = os.getenv('EPOINT_FAILED_REDIRECT_URL')


if not EPOINT_PUBLIC_KEY or not EPOINT_PRIVATE_KEY:
    warn('set EPOINT_PUBLIC_KEY/EPOINT_PRIVATE_KEY env variables to use this library correctly')
