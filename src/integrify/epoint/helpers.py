import base64
import json
from functools import partial
from hashlib import sha1

from integrify.epoint import env
from integrify.epoint.schemas.callback import CallbackDataSchema, DecodedCallbackDataSchema

__all__ = ['generate_signature', 'decode_callback_data']

_sha1 = partial(sha1, usedforsecurity=False)


def generate_signature(data: str) -> str:
    """Sorğu data-sını hash və encode etmək üçün funksiya

    Args:
        data: Sorğu data-sı
    """
    sgn_string = env.EPOINT_PRIVATE_KEY + data + env.EPOINT_PRIVATE_KEY
    return base64.b64encode(_sha1(string=sgn_string.encode()).digest()).decode()


def decode_callback_data(data: CallbackDataSchema) -> DecodedCallbackDataSchema:
    """Callback-də gələn encoded datanı decode və signature verify etmək üçün funksiya

    Args:
        data: Callback datası
    """
    if data.signature != generate_signature(data.data):
        return None  # type: ignore[return-value]

    return DecodedCallbackDataSchema.model_validate(json.loads(base64.b64decode(data.data)))
