from functools import cached_property
from typing import Optional, Type

from integrify.api import APIPayloadHandler, _ResponseT
from integrify.payriff import env
from integrify.payriff.schemas.request import (
    CompleteRequestSchema,
    CreateOrderRequestSchema,
    GetOrderInfoRequestSchema,
    RefundRequestSchema,
)
from integrify.payriff.schemas.response import (
    BaseResponseSchema,
    CreateOrderResponseSchema,
    GetOrderInfoResponseSchema,
    RefundResponseSchema,
)


class BasePayloadHandler(APIPayloadHandler):

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
        super().__init__(CreateOrderRequestSchema, BaseResponseSchema[CreateOrderResponseSchema])


class GetOrderInfoPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(GetOrderInfoRequestSchema, BaseResponseSchema[GetOrderInfoResponseSchema])


class RefundPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(RefundRequestSchema, RefundResponseSchema)


class CompletePayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CompleteRequestSchema, BaseResponseSchema)
