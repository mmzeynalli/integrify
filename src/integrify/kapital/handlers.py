import base64
import json
from functools import cached_property
from typing import Optional, Type

import httpx

from integrify.api import APIPayloadHandler, APIResponse, _ResponseT
from integrify.kapital.env import (
    KAPITAL_PASSWORD,
    KAPITAL_USERNAME,
)
from integrify.kapital.schemas.request import (
    ClearingOrderRequestSchema,
    CreateOrderRequestSchema,
    FullReverseOrderRequestSchema,
    LinkCardTokenRequestSchema,
    OrderInformationRequestSchema,
    OrderWithSavedCardRequestSchema,
    PartialReverseOrderRequestSchema,
    PayAndSaveCardRequestSchema,
    ProcessPaymentWithSavedCardRequestSchema,
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
    LinkCardTokenResponseSchema,
    OrderInformationResponseSchema,
    PartialReverseOrderResponseSchema,
    ProcessPaymentWithSavedCardResponseSchema,
    RefundOrderResponseSchema,
)
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
        credentials = f'{KAPITAL_USERNAME}:{KAPITAL_PASSWORD}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
        }

    def post_handle_payload(self, data):
        if self.data_key:
            return json.dumps({self.data_key: data})

        return json.dumps(data)

    def handle_response(self, resp: httpx.Response) -> APIResponse[_ResponseT]:
        """
        Bu funksiya API-dən gələn cavabı status koduna görə tənzimləyir.
        Əgər status kodu 200-dürsə, gələn cavabı modelə uyğunlaşdırır və APIResponse obyektini qaytarır.
        200-dən fərqli status kodu gələrsə, gələn cavabı modelə uyğunlaşdırır və error obyektini APIResponse obyektinə əlavə edir.
        """  # noqa: E501

        api_resp = APIResponse[BaseResponseSchema].model_validate(resp, from_attributes=True)  # type: ignore[assignment]

        if resp.status_code == 200:
            if self.resp_model:
                data = self.get_response_data(resp.json())
                api_resp.body.data = self.resp_model.model_validate(data, from_attributes=True)  # type: ignore[attr-defined]
            else:
                raise ValueError('Response model (`resp_model`) is not set for this handler.')
        else:
            api_resp.body.error = ErrorResponseBodySchema.model_validate(
                resp.json(), from_attributes=True
            )

        return api_resp  # type: ignore[return-value]

    def get_response_data(self, response_json: dict) -> dict:
        if not self.data_key:
            raise NotImplementedError("Subclasses must define 'response_data_key'")

        return response_json.get(self.data_key, {})


class CreateOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            CreateOrderRequestSchema,
            CreateOrderResponseSchema,
            data_key='order',
        )


class OrderInformationPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            OrderInformationRequestSchema,
            OrderInformationResponseSchema,
            data_key='order',
        )

    def post_handle_payload(self, data):
        return data


class DetailedOrderInformationPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            OrderInformationRequestSchema,
            DetailedOrderInformationResponseSchema,
            data_key='order',
        )

    def post_handle_payload(self, data):
        return data


class RefundOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            RefundOrderRequestSchema,
            RefundOrderResponseSchema,
            data_key='tran',
        )


class SaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            SaveCardRequestSchema,
            CreateOrderResponseSchema,
            data_key='order',
        )


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            PayAndSaveCardRequestSchema,
            CreateOrderResponseSchema,
            data_key='order',
        )


class FullReverseOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            FullReverseOrderRequestSchema,
            FullReverseOrderResponseSchema,
            data_key='tran',
        )


class ClearingOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            ClearingOrderRequestSchema,
            ClearingOrderResponseSchema,
            data_key='tran',
        )


class PartialReverseOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            PartialReverseOrderRequestSchema,
            PartialReverseOrderResponseSchema,
            data_key='tran',
        )


class OrderWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            OrderWithSavedCardRequestSchema,
            CreateOrderResponseSchema,
            data_key='order',
        )


class LinkCardTokenPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            LinkCardTokenRequestSchema,
            LinkCardTokenResponseSchema,
            data_key='order',
        )

    def post_handle_payload(self, data):
        return json.dumps(
            {
                'order': {'initiationEnvKind': 'Server'},
                'token': {'storedId': data['token']},
            }
        )


class ProcessPaymentWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            ProcessPaymentWithSavedCardRequestSchema,
            ProcessPaymentWithSavedCardResponseSchema,
            data_key='tran',
        )
