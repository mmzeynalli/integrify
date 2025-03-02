from functools import cached_property
from typing import Optional, Type

from integrify.api import APIPayloadHandler, _ResponseT
from integrify.payriff import env
from integrify.payriff.schemas.request import CreateOrderRequestSchema
from integrify.payriff.schemas.response import CreateOrderResponseSchema
from integrify.schemas import PayloadBaseModel


class BasePayloadHandler(APIPayloadHandler):
    def __init__(
        self,
        req_model: Type[PayloadBaseModel],
        resp_model: Type[_ResponseT],
        data_key: Optional[str] = None,
    ):
        super().__init__(req_model, resp_model)
        self.data_key = data_key

    @cached_property
    def headers(self):
        return {
            'Authorization': f'{env.PAYRIFF_AUTHORIZATION_KEY}',
            'Content-Type': 'application/json',
        }

    def pre_handle_payload(self, *args, **kwds):
        return {
            'merchant': env.PAYRIFF_MERCHANT_ID,
        }


class CreateOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreateOrderRequestSchema, CreateOrderResponseSchema)
