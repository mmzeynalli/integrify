import base64
import json
from hashlib import sha1

from clientaz.epoint import EPOINT_PRIVATE_KEY
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema


def generate_signature(data: str) -> str:
    sgn_string = EPOINT_PRIVATE_KEY + data + EPOINT_PRIVATE_KEY
    return base64.b64encode(sha1(sgn_string.encode()).digest()).decode()


def decode_callback_data(data: str) -> EPointDecodedCallbackDataSchema:
    return EPointDecodedCallbackDataSchema.model_validate(json.loads(base64.b64decode(data)))
