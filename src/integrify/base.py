from typing import Any, Generic, Optional, TypeVar, get_args
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field

ResponseType = TypeVar('ResponseType', bound=BaseModel)


class ApiResponse(BaseModel, Generic[ResponseType]):
    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: ResponseType
    """Cavab sorğusunun body-si"""


class APISupport:
    def __init__(self, name):
        self.name = name

        self.urls: dict[str, str] = {}  # endpoints
        self.handlers: dict[str, APIHandler] = {}  # Handler for each endpoint

        self.default_handler: Optional[APIHandler] = None
        self.client = httpx.Client(timeout=10)

    def add_url(self, route_name: str, url: str):
        self.urls[route_name] = url

    def set_default_handler(self, handler_class: type['APIHandler']):
        self.default_handler = handler_class()

    def add_handler(self, route_name: str, handler_class: type['APIHandler']):
        self.handlers[route_name] = handler_class()

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name not in self.urls:
                raise

        assert self.base_url

        url = urljoin(self.base_url, self.urls[name])
        handler = self.handlers.get(name, self.default_handler)

        return lambda *args, **kwds: self.req(url, handler, *args, **kwds)

    # The next two functions are sync only
    def req(self, url: str, handler: Optional['APIHandler'], *args, **kwds):
        if handler:
            data = handler.handle_request(*args, **kwds)

        response = self.client.request('POST', url, json=data)

        if handler:
            return handler.handle_response(response)

        return response


class APIHandler(Generic[ResponseType]):
    def __init__(self):
        self.resp_model: type[ResponseType] = get_args(self.__class__.__orig_bases__[0])[0]  # type: ignore[attr-defined]

    def get_headers(self):
        return {}

    def handle_request(self, *args, **kwds):
        """Request payload-i Burda duzeldirik"""
        raise NotImplementedError

    def handle_response(self, resp: httpx.Response):
        """Response-u Burda process edirik"""
        resp.body = resp.json()  # type: ignore[attr-defined]

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
