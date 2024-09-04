import base64
import json

from clientaz.base import RequestType, SyncApiRequest
from clientaz.epoint import EPOINT_PUBLIC_KEY
from clientaz.epoint.helper import generate_signature
from clientaz.logger import EPOINT_LOGGER_NAME


class EPointRequest(SyncApiRequest[RequestType]):
    def __init__(self):
        super().__init__('EPoint', EPOINT_LOGGER_NAME)
        self.base_url = 'https://epoint.az'
        self.data = {
            'public_key': EPOINT_PUBLIC_KEY,
            'language': 'en',
        }

    def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return super().__call__(*args, **kwargs)
