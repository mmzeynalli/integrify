from typing import Any, Callable, Coroutine, Optional
from urllib.parse import urljoin

import httpx

from integrify.logger import LOGGER_FUNCTION
from integrify.schemas import APIResponse, PayloadBaseModel, ResponseType


class APIClient:
    def __init__(
        self,
        name: str,
        base_url: str,
        default_handler: Optional['APIPayloadHandler'] = None,
        sync: bool = True,
    ):
        self.base_url = base_url
        self.default_handler = default_handler or None

        self.request_executor = APIExecutor(name=name, sync=sync)

        self.urls: dict[str, dict[str, str]] = {}  # endpoints
        self.handlers: dict[str, APIPayloadHandler] = {}  # Handler for each endpoint

    def add_url(self, route_name: str, url: str, verb: str):
        self.urls[route_name] = {'url': url, 'verb': verb}

    def set_default_handler(self, handler_class: type['APIPayloadHandler']):
        self.default_handler = handler_class()

    def add_handler(self, route_name: str, handler_class: type['APIPayloadHandler']):
        self.handlers[route_name] = handler_class()

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name not in self.urls:
                raise

        url = urljoin(self.base_url, self.urls[name]['url'])
        verb = self.urls[name]['verb']
        handler = self.handlers.get(name, self.default_handler)

        func = self.request_executor.request_function
        return lambda *args, **kwds: func(url, verb, handler, *args, **kwds)


class APIPayloadHandler:
    def __init__(
        self,
        req_model: Optional[type[PayloadBaseModel]] = None,
        resp_model: Optional[type[ResponseType]] = None,
    ):
        self.req_model = req_model
        self.resp_model = resp_model

    @property
    def headers(self):
        return {}

    def pre_handle_payload(self, *args, **kwds):
        pass

    def handle_payload(self, *args, **kwds):
        if self.req_model:
            return self.req_model.from_args(*args, **kwds).model_dump(
                exclude_none=True,
                mode='json',  # TODO: Maybe serialize Decimal in different way
            )

        raise NotImplementedError

    def post_handle_payload(self, data):
        return data

    def handle_request(self, *args, **kwds):
        pre_data = self.pre_handle_payload(*args, **kwds) or {}
        data = {**pre_data, **self.handle_payload(*args, **kwds)}
        return self.post_handle_payload(data)

    def handle_response(self, resp: httpx.Response) -> APIResponse[ResponseType]:
        if self.resp_model:
            return APIResponse[self.resp_model].model_validate(resp, from_attributes=True)  # type: ignore[name-defined]

        return resp.json()


class APIExecutor:
    def __init__(self, name: str, sync: bool = True):
        self.sync = sync
        self.client_name = name
        self.logger = LOGGER_FUNCTION(name)

        self.client: httpx.Client | httpx.AsyncClient

        if sync:
            self.client = httpx.Client(timeout=10)
        else:
            self.client = httpx.AsyncClient(timeout=10)

    @property
    def request_function(
        self,
    ) -> Callable[
        [str, str, Optional['APIPayloadHandler'], Any],  # input args
        APIResponse[ResponseType] | Coroutine[Any, Any, APIResponse[ResponseType]],  # output
    ]:
        if self.sync:
            return lambda *args, **kwds: self.sync_req(*args, **kwds)
        else:
            return lambda *args, **kwds: self.async_req(*args, **kwds)

    def sync_req(self, url: str, verb: str, handler: Optional['APIPayloadHandler'], *args, **kwds):
        assert isinstance(self.client, httpx.Client)

        data = handler.handle_request(*args, **kwds) if handler else None
        headers = handler.headers if handler else None

        response = self.client.request(verb, url, data=data, headers=headers)

        if not response.is_success:
            self.logger.error(
                f'{self.client_name} request to {url} failed. '
                f'Status code was {response.status_code}. '
                f'Content => {response.content.decode()}'
            )

        if handler:
            return handler.handle_response(response)

        return response

    async def async_req(
        self, url: str, verb: str, handler: Optional['APIPayloadHandler'], *args, **kwds
    ):
        assert isinstance(self.client, httpx.AsyncClient)

        data = handler.handle_request(*args, **kwds) if handler else None
        headers = handler.headers if handler else None

        response = await self.client.request(verb, url, data=data, headers=headers)

        if not response.is_success:
            self.logger.error(
                f'{self.client_name} request to {url} failed. '
                f'Status code was {response.status_code}. '
                f'Content => {response.content.decode()}'
            )

        if handler:
            return handler.handle_response(response)

        return response
