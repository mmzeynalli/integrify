import base64
import json

import httpx

from integrify.api import APIPayloadHandler, APIResponse, ResponseType
from integrify.kapital.env import (
    KAPITAL_PASSWORD,
    KAPITAL_USERNAME,
)
from integrify.kapital.schemas.request import (
    CreateOrderDetails,
    CreateOrderRequestSchema,
)
from integrify.kapital.schemas.response import CreateOrderResponseSchema


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
        order_details = CreateOrderDetails.from_args(*args, **kwds)
        return CreateOrderRequestSchema(order=order_details).model_dump(
            exclude_none=True, by_alias=True, mode='json'
        )

    def handle_request(self, *args, **kwds):
        pre_data = self.pre_handle_payload(*args, **kwds) or {}
        data = {**pre_data, **self.handle_payload(*args, **kwds)}
        return json.dumps(data)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp: APIResponse[CreateOrderResponseSchema] = super().handle_response(resp)  # type: ignore[assignment]

        if resp.status_code == 200:
            api_resp.ok = True

            data = resp.json().get('order', {})

            user_response = CreateOrderResponseSchema(
                id=data['id'],
                password=data['password'],
                redirect_url=f"{data['hppUrl']}?id={data['id']}&password={data['password']}",
            )

            api_resp.body = CreateOrderResponseSchema.model_validate(
                user_response, from_attributes=True
            )
        else:
            api_resp.ok = False

        return api_resp  # type: ignore[return-value]
