import json

from integrify.api import APIPayloadHandler
from integrify.postaguvercini import env
from integrify.postaguvercini.schemas.request import CreditBalanceRequestSchema
from integrify.postaguvercini.schemas.response import CreditBalanceResponseSchema
from integrify.schemas import PayloadBaseModel, _ResponseT


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: type[PayloadBaseModel], resp_model: type[_ResponseT]):
        super().__init__(req_model, resp_model)

    def pre_handle_payload(self, *args, **kwds):
        return {
            'Username': env.POSTA_GUVERCINI_USERNAME,
            'Password': env.POSTA_GUVERCINI_PASSWORD,
        }

    def post_handle_payload(self, data):
        return json.dumps(data)


class CreditBalancePayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreditBalanceRequestSchema, CreditBalanceResponseSchema)
