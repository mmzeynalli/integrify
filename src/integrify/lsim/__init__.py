"""
Dokumentasiya:

EN: https://mmzeynalli.notion.site/LSIM-1974f14f727e8029a3f5f9e4e556afe3?pvs=74
"""

from .bulk.client import LSIMBulkSMSAsyncClient, LSIMBulkSMSClient, LSIMBulkSMSClientClass
from .bulk.env import VERSION as BULKSMS_VERSION
from .single.client import LSIMSingleSMSAsyncClient, LSIMSingleSMSClient, LSIMSingleSMSClientClass
from .single.env import VERSION as SINGLESMS_VERSION

__all__ = [
    'LSIMBulkSMSAsyncClient',
    'LSIMBulkSMSClient',
    'LSIMBulkSMSClientClass',
    'BULKSMS_VERSION',
    'LSIMSingleSMSAsyncClient',
    'LSIMSingleSMSClient',
    'LSIMSingleSMSClientClass',
    'SINGLESMS_VERSION',
]
