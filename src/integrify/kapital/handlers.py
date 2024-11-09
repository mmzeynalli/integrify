import base64
import json
from typing import Type

import httpx

from integrify.api import APIPayloadHandler, APIResponse, ResponseType
from integrify.kapital.env import (
    KAPITAL_PASSWORD,
    KAPITAL_USERNAME,
)
from integrify.kapital.schemas.request import (
    ClearingOrderRequestSchema,
    CreateOrderAndSaveCardRequestSchema,
    CreateOrderRequestSchema,
    FullReverseOrderRequestSchema,
    OrderInformationRequestSchema,
    PartialReverseOrderRequestSchema,
    RefundOrderRequestSchema,
    SaveCardRequestSchema,
)
from integrify.kapital.schemas.response import (
    BaseResponseSchema,
    ClearingOrderResponseSchema,
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    ErrorResponseBodySchema,
    FullReverseOrderResponseSchema,
    OrderInformationResponseSchema,
    PartialReverseOrderResponseSchema,
    RefundOrderResponseSchema,
)
from integrify.schemas import PayloadBaseModel


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: Type[PayloadBaseModel], resp_model: Type[ResponseType]):
        super().__init__(req_model, resp_model)

    @property
    def headers(self):
        credentials = f'{KAPITAL_USERNAME}:{KAPITAL_PASSWORD}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
        }

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp = APIResponse[BaseResponseSchema].model_validate(resp, from_attributes=True)  # type: ignore[assignment]

        if resp.status_code == 200:
            if self.resp_model:
                data = self.get_response_data(resp.json())
                api_resp.body.data = self.resp_model.model_validate(data, from_attributes=True)
            else:
                raise ValueError('Response model (`resp_model`) is not set for this handler.')
        else:
            api_resp.body.error = ErrorResponseBodySchema.model_validate(
                resp.json(), from_attributes=True
            )

        return api_resp  # type: ignore[return-value]

    def get_response_data(self, response_json: dict) -> dict:
        raise NotImplementedError('Must be implemented in subclass.')


class CreateOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreateOrderRequestSchema, BaseResponseSchema)

    def post_handle_payload(self, data):
        return json.dumps({'order': data})

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp = APIResponse[BaseResponseSchema].model_validate(resp, from_attributes=True)  # type: ignore[assignment]

        if resp.status_code == 200:
            data = resp.json().get('order', {})

            api_resp.body.data = CreateOrderResponseSchema(
                id=data['id'],
                password=data['password'],
                redirect_url=f"{data['hppUrl']}?id={data['id']}&password={data['password']}",
            )
        else:
            api_resp.body.error = ErrorResponseBodySchema.model_validate(
                resp.json(), from_attributes=True
            )

        return api_resp  # type: ignore[return-value]


class OrderInformationPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(OrderInformationRequestSchema, OrderInformationResponseSchema)

    def get_response_data(self, response_json: dict) -> dict:
        return response_json.get('order', {})


class DetailedOrderInformationPayloadHandler(OrderInformationPayloadHandler):
    def __init__(self):
        super().__init__(OrderInformationRequestSchema, DetailedOrderInformationResponseSchema)


class RefundOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(RefundOrderRequestSchema, RefundOrderResponseSchema)

    def post_handle_payload(self, data):
        return json.dumps({'tran': data})

    def get_response_data(self, response_json: dict) -> dict:
        return response_json.get('tran', {})


class SaveCardPayloadHandler(CreateOrderPayloadHandler):
    def __init__(self):
        super(BasePayloadHandler, self).__init__(SaveCardRequestSchema, BaseResponseSchema)


class CreateOrderAndSaveCardPayloadHandler(CreateOrderPayloadHandler):
    def __init__(self):
        super(BasePayloadHandler, self).__init__(
            CreateOrderAndSaveCardRequestSchema, BaseResponseSchema
        )


class FullReverseOrderPayloadHandler(RefundOrderPayloadHandler):
    def __init__(self):
        super(BasePayloadHandler, self).__init__(
            FullReverseOrderRequestSchema, FullReverseOrderResponseSchema
        )

    def get_response_data(self, response_json: dict) -> dict:
        return response_json.get('tran', {})


class ClearingOrderPayloadHandler(FullReverseOrderPayloadHandler):
    def __init__(self):
        super(BasePayloadHandler, self).__init__(
            ClearingOrderRequestSchema, ClearingOrderResponseSchema
        )


class PartialReverseOrderPayloadHandler(FullReverseOrderPayloadHandler):
    def __init__(self):
        super(BasePayloadHandler, self).__init__(
            PartialReverseOrderRequestSchema, PartialReverseOrderResponseSchema
        )
