import base64
import json

from integrify.api import APIPayloadHandler, ResponseType
from integrify.epoint import env
from integrify.epoint.helper import generate_signature
from integrify.epoint.schemas.request import (
    GetTransactionStatusInputPayloadSchema,
    PayAndSaveCardInputPayloadSchema,
    PaymentInputPayloadSchema,
    PayoutInputPayloadSchema,
    PayWithSavedCardInputPayloadSchema,
    RefundInputPayloadSchema,
    SaveCardInputPayloadSchema,
    SplitPayAndSaveCardInputPayloadSchema,
    SplitPayInputPayloadSchema,
    SplitPayWithSavedCardInputPayloadSchema,
)
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)
from integrify.schemas import PayloadBaseModel


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: type[PayloadBaseModel], resp_model: type[ResponseType]):
        super().__init__(req_model, resp_model)

    def pre_handle_payload(self, *args, **kwds):
        return {
            'public_key': env.EPOINT_PUBLIC_KEY,
            'language': env.EPOINT_INTERFACE_LANG,
        }

    def post_handle_payload(self, data: dict):
        b64data = base64.b64encode(json.dumps(data).encode()).decode()
        return {
            'data': b64data,
            'signature': generate_signature(b64data),
        }


class PaymentPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PaymentInputPayloadSchema, RedirectUrlResponseSchema)


class GetTransactionStatusPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(GetTransactionStatusInputPayloadSchema, TransactionStatusResponseSchema)


class SaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SaveCardInputPayloadSchema, RedirectUrlWithCardIdResponseSchema)


class PayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayWithSavedCardInputPayloadSchema, BaseResponseSchema)


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayAndSaveCardInputPayloadSchema, RedirectUrlWithCardIdResponseSchema)


class PayoutPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayoutInputPayloadSchema, BaseResponseSchema)


class RefundPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(RefundInputPayloadSchema, MinimalResponseSchema)


class SplitPayPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SplitPayInputPayloadSchema, RedirectUrlResponseSchema)


class SplitPayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            SplitPayWithSavedCardInputPayloadSchema,
            SplitPayWithSavedCardResponseSchema,
        )


class SplitPayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SplitPayAndSaveCardInputPayloadSchema, RedirectUrlWithCardIdResponseSchema)
