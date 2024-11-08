import base64
import json

import httpx

from integrify.api import APIPayloadHandler, APIResponse, ResponseType
from integrify.kapital.env import (
    KAPITAL_PASSWORD,
    KAPITAL_USERNAME,
)
from integrify.kapital.schemas.request import (
    CreateOrderRequestSchema,
    RefundOrderRequestSchema,
)
from integrify.kapital.schemas.response import (
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    OrderInformationResponseSchema,
    RefundOrderResponseSchema,
)


class BasePayloadHandler(APIPayloadHandler):
    @property
    def headers(self):
        credentials = f'{KAPITAL_USERNAME}:{KAPITAL_PASSWORD}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
        }


class CreateOrderPayloadHandler(BasePayloadHandler):
    def handle_payload(self, *args, **kwds):
        order = CreateOrderRequestSchema.from_args(*args, **kwds)
        return {'order': order.model_dump(exclude_none=True, mode='json')}

    def post_handle_payload(self, data):
        return json.dumps(data)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[CreateOrderResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        if resp.status_code == 200:
            api_resp.ok = True

            data = resp.json().get('order', {})

            api_resp.body = CreateOrderResponseSchema(
                id=data['id'],
                password=data['password'],
                redirect_url=f"{data['hppUrl']}?id={data['id']}&password={data['password']}",
            )
        else:
            api_resp.ok = False

        return api_resp  # type: ignore[return-value]


class OrderInformationPayloadHandler(BasePayloadHandler):
    def handle_payload(self, *args, **kwds):
        self.order_id = kwds.get('order_id') or args[0]
        return {}

    def set_urlparams(self, url: str):
        return url.format(order_id=self.order_id)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[OrderInformationResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        if resp.status_code == 200:
            api_resp.ok = True
            api_resp.body = OrderInformationResponseSchema.model_validate(
                resp.json().get('order', {}), from_attributes=True
            )
        else:
            api_resp.ok = False

        return api_resp  # type: ignore[return-value]


class DetailedOrderInformationPayloadHandler(OrderInformationPayloadHandler):
    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[DetailedOrderInformationResponseSchema] = super(
            BasePayloadHandler, self
        ).handle_response(resp)  # type: ignore[assignment]

        if resp.status_code == 200:
            api_resp.ok = True
            api_resp.body = DetailedOrderInformationResponseSchema.model_validate(
                resp.json().get('order', {}), from_attributes=True
            )
        else:
            api_resp.ok = False

        return api_resp  # type: ignore[return-value]


class RefundOrderPayloadHandler(BasePayloadHandler):
    def handle_payload(self, *args, **kwds):
        self.order_id = kwds.get('order_id') or args[0]
        amount = kwds.get('amount') or args[1]

        order = RefundOrderRequestSchema(amount=amount)
        return {'tran': order.model_dump(exclude_none=True, mode='json')}

    def post_handle_payload(self, data):
        return json.dumps(data)

    def set_urlparams(self, url: str):
        return url.format(order_id=self.order_id)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[RefundOrderResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        if resp.status_code == 200:
            api_resp.ok = True
            api_resp.body = RefundOrderResponseSchema.model_validate(
                resp.json().get('tran', {}), from_attributes=True
            )
        else:
            api_resp.ok = False

        return api_resp  # type: ignore[return-value]
