import base64
import json

from integrify.base import AsyncApiRequest, RequestType
from integrify.epoint.helper import generate_signature
from integrify.epoint.sync.base import Request as SyncRequest


class Request(AsyncApiRequest[RequestType], SyncRequest):  # type: ignore[misc]
    """EPoint async sorğular üçün baza class"""

    async def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return await super().__call__(*args, **kwargs)
