import json
from functools import cached_property
from typing import Optional, Type

import httpx
from pydantic import BaseModel

from integrify.api import APIPayloadHandler, APIResponse, _ResponseT
from integrify.kapital.schemas.response import (
    BaseResponseSchema,
    ErrorResponseBodySchema,
)
from integrify.payriff.env import PAYRIFF_AUTHORIZATION_KEY
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
            'Authorization': f'{PAYRIFF_AUTHORIZATION_KEY}',
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

        api_resp = APIResponse[BaseResponseSchema].model_validate(resp, from_attributes=True)

        if resp.status_code == 200:
            if not self.resp_model:
                raise ValueError('Response model is not set for this handler.')

            data = self.get_response_data(resp.json())

            assert issubclass(self.resp_model, BaseModel)
            api_resp.body.data = self.resp_model.model_validate(data, from_attributes=True)
        else:
            api_resp.body.error = ErrorResponseBodySchema.model_validate(
                resp.json(),
                from_attributes=True,
            )

        return api_resp  # type: ignore[return-value]

    def get_response_data(self, response_json: dict) -> dict:
        """`self.data_key` varsa, o key-dəki datanı götürmək"""
        if not self.data_key:
            raise NotImplementedError("Subclasses must define 'response_data_key'")

        return response_json.get(self.data_key, {})
