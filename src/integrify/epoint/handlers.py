import base64
import json

import httpx

from integrify.api import APIPayloadHandler, ResponseType
from integrify.epoint import env
from integrify.epoint.helper import generate_signature
from integrify.epoint.schemas.parts import TransactionStatus, TransactionStatusExtended
from integrify.epoint.schemas.request import (
    GetTransactionStatusRequestSchema,
    PayAndSaveCardRequestSchema,
    PaymentRequestSchema,
    PayoutRequestSchema,
    PayWithSavedCardRequestSchema,
    RefundRequestSchema,
    SaveCardRequestSchema,
    SplitPayAndSaveCardRequestSchema,
    SplitPayRequestSchema,
    SplitPayWithSavedCardRequestSchema,
)
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)
from integrify.schemas import APIResponse, PayloadBaseModel


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

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[MinimalResponseSchema] = super().handle_response(resp)

        # EPoint həmişə 200 qaytarır, error olsa belə
        if isinstance(api_resp.body.status, TransactionStatusExtended):
            api_resp.ok = api_resp.body.status != TransactionStatusExtended.SERVER_ERROR
        else:
            api_resp.ok = api_resp.body.status == TransactionStatus.SUCCESS

        return api_resp  # type: ignore[return-value]


class PaymentPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PaymentRequestSchema, RedirectUrlResponseSchema)


class GetTransactionStatusPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(GetTransactionStatusRequestSchema, TransactionStatusResponseSchema)


class SaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SaveCardRequestSchema, RedirectUrlWithCardIdResponseSchema)


class PayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayWithSavedCardRequestSchema, BaseResponseSchema)


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayAndSaveCardRequestSchema, RedirectUrlWithCardIdResponseSchema)


class PayoutPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(PayoutRequestSchema, BaseResponseSchema)


class RefundPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(RefundRequestSchema, MinimalResponseSchema)


class SplitPayPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SplitPayRequestSchema, RedirectUrlResponseSchema)


class SplitPayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            SplitPayWithSavedCardRequestSchema,
            SplitPayWithSavedCardResponseSchema,
        )


class SplitPayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            SplitPayAndSaveCardRequestSchema,
            RedirectUrlWithCardIdResponseSchema,
        )
