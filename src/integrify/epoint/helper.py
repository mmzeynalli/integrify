import base64
import json
import sys
from functools import partial
from hashlib import sha1

from integrify.epoint import env
from integrify.epoint.schemas.response import CallbackDataSchema, DecodedCallbackDataSchema

__all__ = ['generate_signature', 'decode_callback_data']

# Python 3.8 support
if sys.version_info >= (3, 9):
    _sha1 = partial(sha1, usedforsecurity=False)
else:
    _sha1 = sha1  # pragma: no cover


def generate_signature(data: str) -> str:
    sgn_string = env.EPOINT_PRIVATE_KEY + data + env.EPOINT_PRIVATE_KEY
    return base64.b64encode(_sha1(string=sgn_string.encode()).digest()).decode()


def decode_callback_data(data: CallbackDataSchema) -> DecodedCallbackDataSchema:
    if data.signature != generate_signature(data.data):
        return None  # type: ignore[return-value]

    return DecodedCallbackDataSchema.model_validate(json.loads(base64.b64decode(data.data)))
