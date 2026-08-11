import base64
import json

import httpx

from integrify.api import APIPayloadHandler
from integrify.epoint import env
from integrify.epoint.helpers import generate_signature
from integrify.epoint.schemas.enums import TransactionStatus, TransactionStatusExtended
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
from integrify.schemas import APIResponse, _ResponseT


class BasePayloadHandler(APIPayloadHandler):
    """EPoint üçün baza handler. `req_model`/`resp_model` alt class-larda
    ClassVar kimi təyin olunur."""

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

    def handle_response(self, resp: httpx.Response) -> APIResponse[_ResponseT]:
        api_resp: APIResponse[MinimalResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        # EPoint həmişə 200 qaytarır, error olsa belə
        if isinstance(api_resp.body.status, TransactionStatusExtended):
            api_resp.ok = api_resp.body.status != TransactionStatusExtended.SERVER_ERROR
        else:
            api_resp.ok = api_resp.body.status == TransactionStatus.SUCCESS

        return api_resp  # type: ignore[return-value]


class PaymentPayloadHandler(BasePayloadHandler):
    req_model = PaymentRequestSchema
    resp_model = RedirectUrlResponseSchema


class GetTransactionStatusPayloadHandler(BasePayloadHandler):
    req_model = GetTransactionStatusRequestSchema
    resp_model = TransactionStatusResponseSchema


class SaveCardPayloadHandler(BasePayloadHandler):
    req_model = SaveCardRequestSchema
    resp_model = RedirectUrlWithCardIdResponseSchema


class PayWithSavedCardPayloadHandler(BasePayloadHandler):
    req_model = PayWithSavedCardRequestSchema
    resp_model = BaseResponseSchema


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    req_model = PayAndSaveCardRequestSchema
    resp_model = RedirectUrlWithCardIdResponseSchema


class PayoutPayloadHandler(BasePayloadHandler):
    req_model = PayoutRequestSchema
    resp_model = BaseResponseSchema


class RefundPayloadHandler(BasePayloadHandler):
    req_model = RefundRequestSchema
    resp_model = MinimalResponseSchema


class SplitPayPayloadHandler(BasePayloadHandler):
    req_model = SplitPayRequestSchema
    resp_model = RedirectUrlResponseSchema


class SplitPayWithSavedCardPayloadHandler(BasePayloadHandler):
    req_model = SplitPayWithSavedCardRequestSchema
    resp_model = SplitPayWithSavedCardResponseSchema


class SplitPayAndSaveCardPayloadHandler(BasePayloadHandler):
    req_model = SplitPayAndSaveCardRequestSchema
    resp_model = RedirectUrlWithCardIdResponseSchema
