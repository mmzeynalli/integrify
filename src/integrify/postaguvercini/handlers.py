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
    SendMultipleSMSResponseSchema,
    SendSingleSMSResponseSchema,
    StatusResponseSchema,
)
from integrify.schemas import APIResponse, PayloadBaseModel, _ResponseT


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: type[PayloadBaseModel], resp_model: type[_ResponseT]):
        super().__init__(req_model, resp_model)

    def handle_response(self, resp):
        api_resp: APIResponse[MinimalResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        api_resp.ok = api_resp.body.status_code == 200
        api_resp.status_code = (
            400 if api_resp.body.status_code == 1063 else api_resp.body.status_code
        )

        return api_resp


class SendSingleSMSPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SendSingleSMSRequestSchema, SendSingleSMSResponseSchema)


class SendMultipleSMSPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SendMultipleSMSRequestSchema, SendMultipleSMSResponseSchema)


class StatusPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(StatusRequestSchema, StatusResponseSchema)


class CreditBalancePayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreditBalanceRequestSchema, CreditBalanceResponseSchema)
