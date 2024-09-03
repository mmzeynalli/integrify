import os
from warnings import warn

EPOINT_PUBLIC_KEY: str = os.getenv('EPOINT_PUBLIC_KEY', '')
EPOINT_PRIVATE_KEY: str = os.getenv('EPOINT_PRIVATE_KEY', '')

if not EPOINT_PUBLIC_KEY or not EPOINT_PRIVATE_KEY:
    warn('set EPOINT_PUBLIC_KEY/EPOINT_PRIVATE_KEY env variables to use this library correctly')
