import base64
import json
from hashlib import sha1

from integrify.epoint import EPOINT_PRIVATE_KEY
from integrify.epoint.schemas.types import CallbackDataSchema, DecodedCallbackDataSchema


def generate_signature(data: str) -> str:
    sgn_string = EPOINT_PRIVATE_KEY + data + EPOINT_PRIVATE_KEY
    return base64.b64encode(sha1(sgn_string.encode()).digest()).decode()


def decode_callback_data(data: CallbackDataSchema) -> DecodedCallbackDataSchema:
    if data.signature != generate_signature(data.data):
        return None  # type: ignore[return-value]

    return DecodedCallbackDataSchema.model_validate(json.loads(base64.b64decode(data.data)))
