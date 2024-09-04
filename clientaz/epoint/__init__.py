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
