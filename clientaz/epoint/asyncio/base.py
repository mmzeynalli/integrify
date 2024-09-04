import base64
import json

from clientaz.base import AsyncApiRequest, RequestType
from clientaz.epoint.helper import generate_signature
from clientaz.epoint.sync.base import EPointRequest as SyncEPointRequest


class EPointRequest(AsyncApiRequest[RequestType], SyncEPointRequest):  # type: ignore[misc]
    async def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return await super().__call__(*args, **kwargs)
