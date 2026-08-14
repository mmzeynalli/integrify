import base64
import json
from functools import cached_property
from typing import ClassVar

import httpx
from integrify.api import APIPayloadHandler, APIResponse, _ResponseT
from integrify.kapitalbank.env import KAPITAL_PASSWORD, KAPITAL_USERNAME
from integrify.kapitalbank.schemas.request import (
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
from integrify.kapitalbank.schemas.response import (
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
from pydantic import BaseModel


def _safe_json(resp: httpx.Response) -> dict:
    """Cavabı JSON kimi parse etmək; JSON deyilsə (gateway xətası, boş body)
    exception atmaq əvəzinə boş dict qaytarır."""
    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        return {}

    return data if isinstance(data, dict) else {}


class BasePayloadHandler(APIPayloadHandler):
    """Kapitalbank üçün baza handler. `req_model`/`resp_model`/`data_key`
    alt class-larda ClassVar kimi təyin olunur."""

    data_key: ClassVar[str | None] = None

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
            return {self.data_key: data}

        return data

    def handle_response(self, resp: httpx.Response) -> APIResponse[_ResponseT]:
        """
        Bu funksiya API-dən gələn cavabı status koduna görə tənzimləyir.
        Əgər status kodu 200-dürsə, gələn cavabı modelə uyğunlaşdırır və APIResponse obyektini qaytarır.
        200-dən fərqli status kodu gələrsə, gələn cavabı modelə uyğunlaşdırır və error obyektini APIResponse obyektinə əlavə edir.
        """  # noqa: E501

        api_resp = APIResponse[BaseResponseSchema].model_validate(resp, from_attributes=True)
        body = _safe_json(resp)

        if resp.status_code == 200:
            if not self.resp_model:
                raise ValueError('Response model is not set for this handler.')

            data = self.get_response_data(body)

            assert issubclass(self.resp_model, BaseModel)
            api_resp.body.data = self.resp_model.model_validate(data, from_attributes=True)
        else:
            # Error body gözlənilən formatda olmaya bilər (məs., HTML xəta səhifəsi);
            # bu halda status kodu və `ok` field-i xətanı bildirir.
            try:
                api_resp.body.error = ErrorResponseBodySchema.model_validate(
                    body,
                    from_attributes=True,
                )
            except (ValueError, TypeError):
                api_resp.body.error = None

        return api_resp

    def get_response_data(self, response_json: dict) -> dict:
        """`self.data_key` varsa, o key-dəki datanı götürmək"""
        if not self.data_key:
            raise NotImplementedError("Subclasses must define 'data_key'")

        return response_json.get(self.data_key, {})


class CreateOrderPayloadHandler(BasePayloadHandler):
    req_model = CreateOrderRequestSchema
    resp_model = CreateOrderResponseSchema
    data_key = 'order'


class OrderInformationPayloadHandler(BasePayloadHandler):
    req_model = OrderInformationRequestSchema
    resp_model = OrderInformationResponseSchema
    data_key = 'order'

    def post_handle_payload(self, data):
        return data


class DetailedOrderInformationPayloadHandler(BasePayloadHandler):
    req_model = OrderInformationRequestSchema
    resp_model = DetailedOrderInformationResponseSchema
    data_key = 'order'

    def post_handle_payload(self, data):
        return data


class RefundOrderPayloadHandler(BasePayloadHandler):
    req_model = RefundOrderRequestSchema
    resp_model = RefundOrderResponseSchema
    data_key = 'tran'


class SaveCardPayloadHandler(BasePayloadHandler):
    req_model = SaveCardRequestSchema
    resp_model = CreateOrderResponseSchema
    data_key = 'order'


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    req_model = PayAndSaveCardRequestSchema
    resp_model = CreateOrderResponseSchema
    data_key = 'order'


class FullReverseOrderPayloadHandler(BasePayloadHandler):
    req_model = FullReverseOrderRequestSchema
    resp_model = FullReverseOrderResponseSchema
    data_key = 'tran'


class ClearingOrderPayloadHandler(BasePayloadHandler):
    req_model = ClearingOrderRequestSchema
    resp_model = ClearingOrderResponseSchema
    data_key = 'tran'


class PartialReverseOrderPayloadHandler(BasePayloadHandler):
    req_model = PartialReverseOrderRequestSchema
    resp_model = PartialReverseOrderResponseSchema
    data_key = 'tran'


class OrderWithSavedCardPayloadHandler(BasePayloadHandler):
    req_model = OrderWithSavedCardRequestSchema
    resp_model = CreateOrderResponseSchema
    data_key = 'order'


class LinkCardTokenPayloadHandler(BasePayloadHandler):
    req_model = LinkCardTokenRequestSchema
    resp_model = LinkCardTokenResponseSchema
    data_key = 'order'

    def post_handle_payload(self, data):
        # `dict` qaytarırıq (əvvəlki `json.dumps(...)` string qaytarırdı, bu da httpx
        # tərəfindən ikiqat JSON-encode olunub, body-ni korlayırdı).
        return {
            'order': {'initiationEnvKind': 'Server'},
            'token': {'storedId': data['token']},
        }


class ProcessPaymentWithSavedCardPayloadHandler(BasePayloadHandler):
    req_model = ProcessPaymentWithSavedCardRequestSchema
    resp_model = ProcessPaymentWithSavedCardResponseSchema
    data_key = 'tran'
