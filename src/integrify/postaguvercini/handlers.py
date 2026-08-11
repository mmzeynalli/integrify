from integrify.api import APIPayloadHandler
from integrify.postaguvercini.schemas.request import (
    CreditBalanceRequestSchema,
    SendMultipleSMSRequestSchema,
    SendSingleSMSRequestSchema,
    StatusRequestSchema,
)
from integrify.postaguvercini.schemas.response import (
    CreditBalanceResponseSchema,
    MinimalResponseSchema,
    SendSMSResponseSchema,
    StatusResponseSchema,
)
from integrify.schemas import APIResponse


class BasePayloadHandler(APIPayloadHandler):
    """PostaGuvercini üçün baza handler. `req_model`/`resp_model` alt class-larda
    ClassVar kimi təyin olunur."""

    def handle_response(self, resp):
        api_resp: APIResponse[MinimalResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        api_resp.ok = api_resp.body.status_code == 200
        api_resp.status_code = 500 if api_resp.body.status_code > 500 else api_resp.body.status_code

        return api_resp


class SendSingleSMSPayloadHandler(BasePayloadHandler):
    req_model = SendSingleSMSRequestSchema
    resp_model = SendSMSResponseSchema


class SendMultipleSMSPayloadHandler(BasePayloadHandler):
    req_model = SendMultipleSMSRequestSchema
    resp_model = SendSMSResponseSchema


class StatusPayloadHandler(BasePayloadHandler):
    req_model = StatusRequestSchema
    resp_model = StatusResponseSchema


class CreditBalancePayloadHandler(BasePayloadHandler):
    req_model = CreditBalanceRequestSchema
    resp_model = CreditBalanceResponseSchema
