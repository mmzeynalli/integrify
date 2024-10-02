from typing import Any, Generic, Optional, TypeVar, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field

from integrify.logger import LOGGER_FUNCTION

ResponseType = TypeVar('ResponseType', bound=BaseModel)
RequestType = TypeVar('RequestType')


class ApiResponse(BaseModel, Generic[ResponseType]):
    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: ResponseType
    """Cavab sorğusunun body-si"""


def send_request(func):
    def wrapper(self, *args, **kwargs) -> ApiResponse[ResponseType]:
        func(self, *args, **kwargs)
        return self.__call__()

    return wrapper


class ApiRequest:
    session: Union[httpx.Client, httpx.AsyncClient, None] = None

    def __init__(self, client_name: str, logger_name: str):
        self.base_url: str
        self.path: str
        self.verb: Optional[str] = None
        self.headers: dict = {}
        self.body: dict = {}

        #
        self.client_name: str = client_name
        self.logger = LOGGER_FUNCTION(logger_name)

        self.resp_model: type[ResponseType]  # type: ignore[valid-type]
        self.accept_status_codes: list[int] = [200, 201, 204]

    @property
    def url(self):
        return urljoin(self.base_url, self.path)

    def process_response(self, resp: httpx.Response):
        resp.body = resp.json()  # type: ignore[attr-defined]

        if not resp.is_success:
            self.logger.error(
                f'{self.client_name} failed. Status code was {resp.status_code}. '
                f'Content => {resp.body}'  # type: ignore[attr-defined]
            )
        elif resp.status_code not in self.accept_status_codes:
            self.logger.error(
                f'{self.client_name} response is not in {self.accept_status_codes}. '
                f'Status: {resp.status_code}, body: {resp.body}'  # type: ignore[attr-defined]
            )

        return ApiResponse[self.resp_model].model_validate(resp, from_attributes=True)  # type: ignore[name-defined]

    def __call__(self, *args: Any, **kwds: Any): ...


class SyncApiRequest(ApiRequest):
    session: Optional[httpx.Client] = None

    def __call__(self, *args: Any, **kwds: Any):
        if not self.session:
            self.session = httpx.Client(timeout=10)

        resp = self.session.request(self.verb, self.url, data=self.body, headers=self.headers)  # type: ignore[arg-type]
        return self.process_response(resp)


class AsyncApiRequest(ApiRequest):
    session: Optional[httpx.AsyncClient] = None

    async def __call__(self, *args, **kwds):
        if not self.session:
            self.session = httpx.AsyncClient(timeout=10)

        resp = await self.session.request(
            self.verb,
            self.url,
            data=self.body,
            headers=self.headers,
        )
        return self.process_response(resp)
