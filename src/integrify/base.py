from typing import Any, Generic, Optional, TypeVar
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field, field_validator

RequestType = TypeVar('RequestType', bound=BaseModel)
ResponseType = TypeVar('ResponseType', bound=BaseModel)


class ApiResponse(BaseModel, Generic[ResponseType]):
    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: ResponseType = Field(validation_alias='content')
    """Cavab sorğusunun body-si"""

    @field_validator('body', mode='before')
    def convert_to_dict(cls, v: str | bytes | dict) -> dict:
        if isinstance(v, dict):  # in tests
            return v

        import json

        return json.loads(v)


class APISupport:
    def __init__(
        self,
        base_url: str,
        default_handler: Optional['APIHandler'] = None,
        sync: bool = True,
    ):
        self.base_url = base_url
        self.default_handler = default_handler or None

        self.urls: dict[str, str] = {}  # endpoints
        self.handlers: dict[str, APIHandler] = {}  # Handler for each endpoint

        self.sync = sync

        if sync:
            self.client = httpx.Client(timeout=10)
        else:
            self.client = httpx.AsyncClient(timeout=10)

    def add_url(self, route_name: str, url: str):
        self.urls[route_name] = url

    # def set_default_handler(self, handler_class: type['APIHandler']):
    #     self.default_handler = handler_class()

    def add_handler(self, route_name: str, handler_class: type['APIHandler']):
        self.handlers[route_name] = handler_class()  # type: ignore[call-arg]

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name not in self.urls:
                raise

        assert self.base_url

        url = urljoin(self.base_url, self.urls[name])
        handler = self.handlers.get(name, self.default_handler)

        if self.sync:
            return lambda *args, **kwds: self.sync_req(url, handler, *args, **kwds)  # type: ignore[arg-type]
        else:
            return lambda *args, **kwds: self.async_req(url, handler, *args, **kwds)  # type: ignore[arg-type]

    # The next two functions are sync only
    def sync_req(self, url: str, handler: 'APIHandler', *args, **kwds):  # FIXME
        assert isinstance(self.client, httpx.Client)

        if handler:
            data = handler.handle_request(*args, **kwds)

        response = self.client.request(handler.verb, url, data=data, headers=handler.headers)

        if handler:
            return handler.handle_response(response)

        return response

    async def async_req(self, url: str, handler: 'APIHandler', *args, **kwds):  # FIXME
        assert isinstance(self.client, httpx.AsyncClient)

        if handler:
            data = handler.handle_request(*args, **kwds)

        response = await self.client.request(handler.verb, url, data=data, headers=handler.headers)

        if handler:
            return handler.handle_response(response)

        return response


class APIHandler:
    def __init__(self, verb: str, req_model: type[RequestType], resp_model: type[ResponseType]):
        self.verb = verb
        self.req_model = req_model
        self.resp_model = resp_model

    @property
    def headers(self):
        return {}

    def pre_handle_payload(self, *args, **kwds):
        pass

    def handle_payload(self, *args, **kwds):
        """Request payload-i Burda duzeldirik"""
        return {}

    def post_handle_payload(self, *args, **kwds):
        pass

    def handle_request(self, *args, **kwds):
        data = {**self.pre_handle_payload(*args, **kwds), **self.handle_payload(*args, **kwds)}
        return self.post_handle_payload(data)

    def handle_response(self, resp: httpx.Response) -> ApiResponse[ResponseType]:
        """Response-u Burda process edirik"""
        # if not resp.is_success:
        #     self.logger.error(
        #         f'{self.client_name} failed. Status code was {resp.status_code}. '
        #         f'Content => {resp.body}'  # type: ignore[attr-defined]
        #     )
        # elif resp.status_code not in self.accept_status_codes:
        #     self.logger.error(
        #         f'{self.client_name} response is not in {self.accept_status_codes}. '
        #         f'Status: {resp.status_code}, body: {resp.body}'  # type: ignore[attr-defined]
        #     )

        return ApiResponse[self.resp_model].model_validate(resp, from_attributes=True)  # type: ignore[name-defined]
