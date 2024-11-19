import base64
import json
from typing import Optional, Type

import httpx

from integrify.api import APIPayloadHandler, APIResponse, ResponseType
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
        resp_model: Type[ResponseType],
        req_data_key: Optional[str] = None,
        resp_data_key: Optional[str] = None,
    ):
        super().__init__(req_model, resp_model)
        self.req_data_key = req_data_key
        self.resp_data_key = resp_data_key

    @property
    def headers(self):
        credentials = f'{KAPITAL_USERNAME}:{KAPITAL_PASSWORD}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
        }

    def post_handle_payload(self, data):
        if self.req_data_key:
            return json.dumps({self.req_data_key: data})

        return json.dumps(data)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        """
        Bu funksiya API-dən gələn cavabı status koduna görə tənzimləyir.
        Əgər status kodu 200-dürsə, gələn cavabı modelə uyğunlaşdırır və APIResponse obyektini qaytarır.
        200-dən fərqli status kodu gələrsə, gələn cavabı modelə uyğunlaşdırır və error obyektini APIResponse obyektinə əlavə edir.
        """  # noqa: E501

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

    def process_order_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        """
        CreateOrderPayloadHandler üçün xüsusi funksiya.
        Bu funksiyada response-da gelen order id ve password-dan istifadə edərək redirect_url yaradılır.
        """  # noqa: E501
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

    def get_response_data(self, response_json: dict) -> dict:
        if not self.resp_data_key:
            raise NotImplementedError("Subclasses must define 'response_data_key'")

        return response_json.get(self.resp_data_key, {})


class CreateOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(CreateOrderRequestSchema, BaseResponseSchema, req_data_key='order')

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        return self.process_order_response(resp)


class OrderInformationPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            OrderInformationRequestSchema,
            OrderInformationResponseSchema,
            resp_data_key='order',
        )

    def post_handle_payload(self, data):
        return data


class DetailedOrderInformationPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            OrderInformationRequestSchema,
            DetailedOrderInformationResponseSchema,
            resp_data_key='order',
        )

    def post_handle_payload(self, data):
        return data


class RefundOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            RefundOrderRequestSchema,
            RefundOrderResponseSchema,
            req_data_key='tran',
            resp_data_key='tran',
        )


class SaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            SaveCardRequestSchema,
            BaseResponseSchema,
            req_data_key='order',
        )

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        return self.process_order_response(resp)


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            PayAndSaveCardRequestSchema,
            BaseResponseSchema,
            req_data_key='order',
        )

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        return self.process_order_response(resp)


class FullReverseOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            FullReverseOrderRequestSchema,
            FullReverseOrderResponseSchema,
            req_data_key='tran',
            resp_data_key='tran',
        )


class ClearingOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            ClearingOrderRequestSchema,
            ClearingOrderResponseSchema,
            req_data_key='tran',
            resp_data_key='tran',
        )


class PartialReverseOrderPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            PartialReverseOrderRequestSchema,
            PartialReverseOrderResponseSchema,
            req_data_key='tran',
            resp_data_key='tran',
        )


class OrderWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(OrderWithSavedCardRequestSchema, BaseResponseSchema, req_data_key='order')

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        return self.process_order_response(resp)


class LinkCardTokenPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(
            LinkCardTokenRequestSchema,
            LinkCardTokenResponseSchema,
            resp_data_key='order',
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
            req_data_key='tran',
            resp_data_key='tran',
        )
