import string
from functools import cached_property
from typing import Any, Callable, Coroutine, Optional, Union
from urllib.parse import urljoin

import httpx

from integrify.logger import LOGGER_FUNCTION
from integrify.schemas import APIResponse, DryResponse, PayloadBaseModel
from integrify.utils import _UNSET, _ResponseT


class APIClient:
    """
    API inteqrasiyaları üçün klient
    """

    def __init__(
        self,
        name: str,
        base_url: Optional[str] = None,
        default_handler: Optional['APIPayloadHandler'] = None,
        sync: bool = True,
        dry: bool = False,
    ):
        """
        Args:
            name: Klient adı. Logging üçün istifadə olunur.
            base_url: API-lərin əsas (kök) url-i. Əgər bir neçə base_url varsa, bu field-i
                boş saxlayıb, hər endpoint-ə uyğun base_url-i `add_url` funksiyasında
                verin.
            default_handler: default API handler. Bu handler əgər hər hansı bir API-yə
                handler register olunmadıqda istifadə olunur.
            sync: Sync (True) və ya Async (False) klient seçimi. Default olaraq sync seçilir.
        """
        self.base_url = base_url
        self.default_handler = default_handler or APIPayloadHandler(None, None)

        self.request_executor = APIExecutor(name=name, sync=sync, dry=dry)
        """API sorğularını icra edən obyekt"""

        self.urls: dict[str, dict[str, str]] = {}
        """API sorğularının endpoint və metodunun mapping-i"""

        self.handlers: dict[str, APIPayloadHandler] = {}
        """API sorğularının payload (request və response) handler-lərının mapping-i"""

    def add_url(self, route_name: str, url: str, verb: str, base_url: Optional[str] = None) -> None:
        """Yeni endpoint əlavə etmə funksiyası

        Args:
            route_name: Funksionallığın adı (məs., `pay`, `refund` və s.)
            url: Endpoint url-i
            verb: Endpoint metodunun (`POST`, `GET`, və s.)
        """
        self.urls[route_name] = {'url': url, 'verb': verb}

        # Əgər inteqrasiyanın bütün endpoint-ləri bir base_url-də deyilsə,
        # endpointləri, `base_url` ilə əlavə etmək lazımdır.
        if base_url:
            self.urls[route_name]['base_url'] = base_url

    def set_default_handler(self, handler_class: type['APIPayloadHandler']) -> None:
        """Sorğulara default handler setter-i

        Args:
            handler_class: Default handler class-ı
        """
        self.default_handler = handler_class()  # pragma: no cover

    def add_handler(self, route_name: str, handler_class: type['APIPayloadHandler']) -> None:
        """Endpoint-ə handler əlavə etmək method-u

        Args:
            route_name: Funksionallığın adı (məs., `pay`, `refund` və s.)
            handler_class: Həmin sorğunun (və response-unun) payload handler class-ı
        """
        self.handlers[route_name] = handler_class()

    def __getattribute__(self, name: str) -> Any:
        """Möcüzənin baş verdiyi yer:

        Bu kitanxanada, heç bir inteqrasiya üçün birbaşa funksiya mövcud deyil. Bunun yerinə,
        bu dunder metodundan istifadə edərək, hansı endpointə nə sorğu atılacağını anlaya bilirik.
        """
        try:
            return super().__getattribute__(name)
        except AttributeError:
            # Əgər "axtarılan" funksiyanın adı `self.urls` listimizdə mövcud deyilsə,
            # exception qaldırırıq
            if name not in self.urls:
                raise

            # "Axtarılan" funksiyanın adından istifadə edərək, lazımi endpoint, metod və handler-i
            # taparaq, sorğunu icra edirik.
            base_url = self.base_url or self.urls[name]['base_url']
            url = urljoin(base_url, self.urls[name]['url'])
            verb = self.urls[name]['verb']
            handler = self.handlers.get(name, self.default_handler)

            func = self.request_executor.request_function
            return lambda *args, **kwds: func(
                url,
                verb,
                handler,
                # Exclude unset values, to trigger pydantic defaults
                *(arg for arg in args if arg is not _UNSET),
                **{k: v for k, v in kwds.items() if v is not _UNSET},
            )


class APIPayloadHandler:
    """Sorğu və cavab data payload-ları üçün handler class-ı"""

    def __init__(
        self,
        req_model: Optional[type[PayloadBaseModel]] = None,
        resp_model: Union[type[_ResponseT], type[dict], None] = dict,
        dry: bool = False,
    ):
        """
        Args:
            req_model: Sorğunun payload model-i
            resp_model: Sorğunun cavabının payload model-i
            dry: Simulasiya bool-u: True olarsa, sorğu göndərilmir, göndərilən data qaytarılır
        """
        self.req_model = req_model
        self.__req_model: Optional[PayloadBaseModel] = None  # initialized pydantic model
        self.resp_model = resp_model
        self.dry = dry

    def set_urlparams(self, url: str) -> str:
        """URL-in query-param-larını set etmək üçün funksiya (əgər varsa)

        Args:
            url: Format olunmalı url
        """
        if not (self.req_model and self.req_model.URL_PARAM_FIELDS and self.__req_model):
            if any(tup[1] for tup in string.Formatter().parse(url) if tup[1] is not None):
                raise ValueError('URL should not expect any arguments')

            return url

        return url.format(
            **self.__req_model.model_dump(
                by_alias=True,
                include=self.req_model.URL_PARAM_FIELDS,
                exclude_none=True,
                mode='json',
            )
        )

    @cached_property
    def headers(self) -> dict:
        """Sorğunun header-ləri"""
        return {'Content-Type': 'application/json'}

    @cached_property
    def req_args(self) -> dict:
        """Request funksiyası üçün əlavə parametrlər"""
        return {}

    def pre_handle_payload(self, *args, **kwds):
        """Sorğunun payload-ının pre-processing-i. Əgər istənilən payload-a
        əlavə datanı lazımdırsa (bütün sorğularda eyni olan data), bu funksiyadan
        istifadə edə bilərsiniz.

        Misal üçün: Bax [`EPointClientClass`][integrify.epoint.client.EPointClientClass]
        """

    def handle_payload(self, *args, **kwds):
        """Verilən argumentləri `self.req_model` formatında payload-a çevirən funksiya.
        `self.req_model` qeyd edilməyibsə, bu funksiya override olunmalıdır (!).
        """
        if self.req_model:
            self.__req_model = self.req_model.from_args(*args, **kwds)
            return self.__req_model.model_dump(
                by_alias=True,
                exclude=self.req_model.URL_PARAM_FIELDS,
                exclude_none=True,
                mode='json',
            )

        # `req_model` yoxdursa, o zaman `*args` boş olmalıdır, çünki onların key-ləri bilinmir
        assert not args

        return kwds

    def post_handle_payload(self, data: Any):
        """Sorğunun payload-ının post-processing-i. Əgər sorğu göndərməmişdən qabaq
        son datanın üzərinə əlavələr lazımdırsa, bu funksiyadan istifadə edə bilərsiniz.

        Misal üçün: Bax [`EPointClientClass`][integrify.epoint.client.EPointClientClass]

        Args:
            data: `pre_handle_payload` və `handle_payload` funksiyalarından yaradılmış data.
        """
        return data  # pragma: no cover

    def handle_request(self, *args, **kwds):
        """Sorğu üçün payload-u hazırlayan funksiya. Üç mərhələ icra edir,
        və bu mərhələlər override oluna bilər. (Misal üçün:
        Bax [`EPointClientClass`][integrify.epoint.client.EPointClientClass])

        1. Pre-processing
        2. Payload hazırlama
        3. Post-processing
        """

        pre_data = self.pre_handle_payload(*args, **kwds) or {}
        data = {**pre_data, **self.handle_payload(*args, **kwds)}
        return self.post_handle_payload(data)

    def handle_response(
        self,
        resp: httpx.Response,
    ) -> Union[APIResponse[_ResponseT], httpx.Response]:
        """Sorğudan gələn cavab payload-ı handle edən funksiya. `self.resp_model` schema-sı
        verilibsə, onunla parse və validate olunur, əks halda, json/dict formatında qaytarılır.
        """
        if not self.resp_model:
            return resp

        return APIResponse[self.resp_model].model_validate(resp, from_attributes=True)  # type: ignore[name-defined]


class APIExecutor:
    """API sorgularını icra edən class"""

    def __init__(self, name: str, sync: bool = True, dry: bool = False):
        """
        Args:
            name: API klientin adı. Logging üçün istifadə olunur.
            sync: Sync (True) və ya Async (False) klient seçimi. Default olaraq sync seçilir.
            dry: Sorğu göndərmək əvəzinə göndəriləcək datanı qaytarmaq üçün istifadə olunur.
                    Debug üçün nəzərdə tutulub.
        """
        self.sync = sync
        self.dry = dry
        self.client_name = name
        self.logger = LOGGER_FUNCTION(name)

        self.client: Union[httpx.Client, httpx.AsyncClient]
        """httpx sorğu client-i"""

        if sync:
            self.client = httpx.Client(timeout=10)
        else:
            self.client = httpx.AsyncClient(timeout=10)

    @property
    def request_function(
        self,
    ) -> Callable[
        [str, str, APIPayloadHandler, Any],  # input args
        Union[
            Union[httpx.Response, APIResponse[_ResponseT], DryResponse],
            Coroutine[
                Any,
                Any,
                Union[httpx.Response, APIResponse[_ResponseT], DryResponse],
            ],
        ],  # output
    ]:
        """Sync/async request atan funksiyanı seçən attribute"""
        if self.sync:
            return self.sync_req

        return self.async_req  # pragma: no cover

    def sync_req(
        self,
        url: str,
        verb: str,
        handler: APIPayloadHandler,
        *args,
        **kwds,
    ) -> Union[httpx.Response, APIResponse[_ResponseT], DryResponse]:
        """Sync sorğu atan funksiya

        Args:
            url: Sorğunun full url-i
            verb: Sorğunun metodun (`POST`, `GET`, və s.)
            handler: Sorğu və cavabın payload handler-i
        """
        assert isinstance(self.client, httpx.Client)

        data = handler.handle_request(*args, **kwds)
        headers = handler.headers
        full_url = handler.set_urlparams(url)

        if self.dry or handler.dry:
            return DryResponse(  # type: ignore[return-value]
                url=full_url,
                verb=verb,
                request_args=handler.req_args,
                headers=headers,
                data=data,
            )

        request_kwds = {'headers': headers, **handler.req_args}

        if verb == 'GET':
            request_kwds['params'] = data
        else:
            request_kwds['json'] = data

        response = self.client.request(verb, full_url, **request_kwds)

        if not response.is_success:
            self.logger.error(
                '%s request to %s failed. Status code was %d. Content => %s',
                self.client_name,
                url,
                response.status_code,
                response.content.decode(),
            )

        return handler.handle_response(response)

    async def async_req(  # pragma: no cover
        self,
        url: str,
        verb: str,
        handler: APIPayloadHandler,
        *args,
        **kwds,
    ) -> Union[httpx.Response, APIResponse[_ResponseT], DryResponse]:
        """Async sorğu atan funksiya

        Args:
            url: Sorğunun full url-i
            verb: Sorğunun metodun (`POST`, `GET`, və s.)
            handler: Sorğu və cavabın payload handler-i
        """
        assert isinstance(self.client, httpx.AsyncClient)

        data = handler.handle_request(*args, **kwds)
        headers = handler.headers
        full_url = handler.set_urlparams(url)

        if self.dry:
            # Sorğu göndərmək əvəzinə göndəriləcək datanı qaytarmaq
            return DryResponse(  # type: ignore[return-value]
                url=full_url,
                verb=verb,
                request_args=handler.req_args,
                headers=headers,
                data=data,
            )

        request_kwds = {'headers': headers, **handler.req_args}

        if verb == 'GET':
            request_kwds['params'] = data
        else:
            request_kwds['json'] = data

        response = await self.client.request(verb, full_url, **request_kwds)

        if not response.is_success:
            self.logger.error(
                '%s request to %s failed. Status code was %d. Content => %s',
                self.client_name,
                url,
                response.status_code,
                response.content.decode(),
            )

        return handler.handle_response(response)
