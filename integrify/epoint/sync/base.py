import base64
import json

from integrify.base import RequestType, SyncApiRequest
from integrify.epoint import EPOINT_INTERFACE_LANG, EPOINT_LOGGER_NAME, EPOINT_PUBLIC_KEY
from integrify.epoint.helper import generate_signature


class Request(SyncApiRequest[RequestType]):
    """EPoint sorğular üçün baza class"""

    def __init__(self):
        super().__init__('EPoint', EPOINT_LOGGER_NAME)
        self.base_url = 'https://epoint.az'
        self.data = {
            'public_key': EPOINT_PUBLIC_KEY,
            'language': EPOINT_INTERFACE_LANG,
        }

    def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return super().__call__(*args, **kwargs)
