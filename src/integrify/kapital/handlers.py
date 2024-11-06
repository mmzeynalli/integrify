import base64
import json
import httpx
from typing import Type

from integrify.api import APIPayloadHandler, APIResponse, ResponseType
from integrify.schemas import PayloadBaseModel
from integrify.kapital.env import (
    KAPITAL_USERNAME,
    KAPITAL_PASSWORD,
)
from integrify.kapital.schemas.request import (
    CreateOrderDetails,
    CreateOrderRequestSchema,
)
from integrify.kapital.schemas.response import CreateOrderResponseSchema


class BasePayloadHandler(APIPayloadHandler):

    @property
    def headers(self):
        credentials = f"{KAPITAL_USERNAME}:{KAPITAL_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }


class CreateOrderPayloadHandler(BasePayloadHandler):

    def handle_payload(self, *args, **kwds):
        order_details = CreateOrderDetails.from_args(*args, **kwds)
        return CreateOrderRequestSchema(order=order_details).model_dump(
            exclude_none=True, by_alias=True, mode="json"
        )

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        api_resp = super().handle_response(resp)

        if resp.status_code == 200:
            api_resp.ok = True

            data = resp.json().get("order", {})

            user_response = CreateOrderResponseSchema(
                id=data["id"],
                password=data["password"],
                redirect_url=f"{data['hppUrl']}?id={data['id']}&password={data['password']}",
            )

            api_resp.body = CreateOrderResponseSchema.model_validate(
                user_response, from_attributes=True
            )
        else:
            api_resp.ok = False

        return api_resp
