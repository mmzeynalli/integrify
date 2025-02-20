from integrify.api import APIPayloadHandler
from integrify.postaguvercini import env
from integrify.postaguvercini.schemas.request import (
    CreditBalanceRequestSchema,
    SendMultipleSMSRequestSchema,
    SendSingleSMSRequestSchema,
)
from integrify.postaguvercini.schemas.response import (
    CreditBalanceResponseSchema,
    MinimalResponseSchema,
    SendMultipleSMSResponseSchema,
    SendSingleSMSResponseSchema,
)
from integrify.schemas import APIResponse, PayloadBaseModel, _ResponseT


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: type[PayloadBaseModel], resp_model: type[_ResponseT]):
        super().__init__(req_model, resp_model)

    def pre_handle_payload(self, *args, **kwds):
        return {
            'Username': env.POSTA_GUVERCINI_USERNAME,
            'Password': env.POSTA_GUVERCINI_PASSWORD,
        }

    def handle_response(self, resp):
        api_resp: APIResponse[MinimalResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        # Status kodu hemise 200 gelir
        # Body-in icindeki status kodu ise, ferqli araliqlarda olur

        return api_resp


class SendSingleSMSPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SendSingleSMSRequestSchema, SendSingleSMSResponseSchema)


class SendMultipleSMSPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(SendMultipleSMSRequestSchema, SendMultipleSMSResponseSchema)


class CreditBalancePayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreditBalanceRequestSchema, CreditBalanceResponseSchema)
