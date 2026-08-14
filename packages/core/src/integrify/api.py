import string
from collections.abc import Callable, Coroutine
from functools import cached_property
from typing import Any, ClassVar, Optional, TypeVar
from urllib.parse import urljoin

import httpx
from integrify.logger import LOGGER_FUNCTION
from integrify.schemas import APIResponse, DryResponse, PayloadBaseModel
from integrify.utils import UNSET, _ResponseT

DEFAULT_TIMEOUT = 10
"""Default sorğu timeout-u (saniyə ilə)"""


# ------------------------------------------------------------------------------------------------ #
# Sync/async üçün tip markerləri                                                                   #
# ------------------------------------------------------------------------------------------------ #
# Bunlar yalnız tip səviyyəsində istifadə olunur (runtime-da heç bir rol oynamır). İnteqrasiya
# klientləri `Generic[_Mode]` ilə parametrləşdirilib, hər metod üçün iki `@overload` təyin edir:
# `self: XClientClass[_Sync]`  -> sync qaytarış (APIResponse[...])
# `self: XClientClass[_Async]` -> async qaytarış (Coroutine[Any, Any, APIResponse[...]])
# Beləliklə, sync və async klientlər eyni docstring-i paylaşır,
# lakin düzgün qaytarış tipinə malikdir.


class _Sync:  # pylint: disable=too-few-public-methods
    """Sync klient rejimi üçün tip markeri (yalnız type-checking)."""


class _Async:  # pylint: disable=too-few-public-methods
    """Async klient rejimi üçün tip markeri (yalnız type-checking)."""


_Mode = TypeVar('_Mode')
"""İnteqrasiya klientlərinin sync/async rejimini bildirən TypeVar (`_Sync` və ya `_Async`)."""


class APIClient:
    """
    API inteqrasiyaları üçün klient
    """

    def __init__(
        self,
        name: str,
        base_url: str | None = None,
        default_handler: Optional['APIPayloadHandler'] = None,
        sync: bool = True,
        dry: bool = False,
        timeout: float | None = DEFAULT_TIMEOUT,
    ):
        """
        Args:
            name: Klient adı. Logging üçün istifadə olunur.
            base_url: API-lərin əsas (kök) url-i. Əgər bir neçə base_url varsa, bu field-i
                boş saxlayıb, hər endpoint-ə uyğun base_url-i `add_url` funksiyasında
                verin. (bax: AzeriCard)
            default_handler: default API handler. Bu handler əgər hər hansı bir API-yə
                handler register olunmadıqda istifadə olunur.
            sync: Sync (True) və ya Async (False) klient seçimi. Default olaraq sync seçilir.
            dry: Sorğu göndərmək əvəzinə göndəriləcək datanı qaytarmaq üçün istifadə olunur.
            timeout: httpx sorğu timeout-u (saniyə ilə).
        """
        self.base_url = base_url
        self.default_handler = default_handler or APIPayloadHandler(None, None)

        self.request_executor = APIExecutor(name=name, sync=sync, dry=dry, timeout=timeout)
        """API sorğularını icra edən obyekt"""

        self.urls: dict[str, dict[str, str]] = {}
        """API sorğularının endpoint və metodunun mapping-i"""

        self.handlers: dict[str, APIPayloadHandler] = {}
        """API sorğularının payload (request və response) handler-lərının mapping-i"""

    def add_url(self, route_name: str, url: str, verb: str, base_url: str | None = None) -> None:
        """Yeni endpoint əlavə etmə funksiyası

        Args:
            route_name: Funksionallığın adı (məs., `pay`, `refund` və s.)
            url: Endpoint url-i
            verb: Endpoint metodu (`POST`, `GET`, və s.)
            base_url: Endpoint-lərin baza (kök) url-i. Endpoint-lər fərqli hostlar
                    üzərində qurulduqda lazım olur.
        """
        self.urls[route_name] = {'url': url, 'verb': verb}

        # Əgər inteqrasiyanın bütün endpoint-ləri bir base_url-də deyilsə,
        # endpointləri, `base_url` ilə əlavə etmək lazımdır.
        self.urls[route_name]['base_url'] = base_url or self.base_url or ''

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

    def close(self) -> None:
        """Sync klientin bağlanması (httpx connection pool-un boşaldılması)"""
        self.request_executor.close()

    async def aclose(self) -> None:
        """Async klientin bağlanması (httpx connection pool-un boşaldılması)"""
        await self.request_executor.aclose()

    def __enter__(self) -> 'APIClient':
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    async def __aenter__(self) -> 'APIClient':
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()

    def _build_request_lambda(
        self,
        func: Callable,
        url: str,
        verb: str,
        handler: 'APIPayloadHandler',
    ) -> Callable:
        return lambda *args, **kwds: func(
            url,
            verb,
            handler,
            *(arg for arg in args if arg is not UNSET),
            **{k: v for k, v in kwds.items() if v is not UNSET},
        )

    def __getattr__(self, name: str) -> Any:
        """Möcüzənin baş verdiyi yer:

        Bu kitanxanada, heç bir inteqrasiya üçün birbaşa funksiya mövcud deyil. Bunun yerinə,
        bu dunder metodundan istifadə edərək, hansı endpointə nə sorğu atılacağını anlaya bilirik.

        `__getattr__` yalnız adi atribut axtarışı uğursuz olduqda çağırılır, ona görə də
        real atributlara (`urls`, `handlers` və s.) heç bir əlavə yük gətirmir.
        """
        # `self.urls`-ə birbaşa müraciət rekursiyaya səbəb ola bilər (əgər hələ init
        # olunmayıbsa), ona görə `__dict__`-dən oxuyuruq.
        urls = self.__dict__.get('urls')

        # "Axtarılan" funksiyanın adı `self.urls` listimizdə mövcud deyilsə, exception qaldırırıq
        if not urls or name not in urls:
            raise AttributeError(name)

        # "Axtarılan" funksiyanın adından istifadə edərək, lazımi endpoint, metod və handler-i
        # taparaq, sorğunu icra edirik.
        base_url = urls[name]['base_url']
        url = urljoin(base_url, urls[name]['url'])
        verb = urls[name]['verb']
        handler = self.handlers.get(name, self.default_handler)

        func = self.request_executor.request_function
        return self._build_request_lambda(func, url, verb, handler)


class APIPayloadHandler:
    """Sorğu və cavab data payload-ları üçün handler class-ı

    Handler-lər **stateless**-dir: sorğu modeli heç vaxt `self`-də saxlanılmır, hər
    çağırışda lokal olaraq yaradılıb ötürülür. Bu, eyni handler instansiyasının
    (məs., `EPointAsyncRequest` kimi shared klientlərdə) paralel sorğularda təhlükəsiz
    istifadəsinə imkan verir.

    `req_model`, `resp_model` və `dry` class atribut (ClassVar) kimi təyin oluna bilər::

        class MyHandler(APIPayloadHandler):
            req_model = MyRequestSchema
            resp_model = MyResponseSchema

    və ya geriyə uyğunluq üçün `__init__`-ə ötürülə bilər.
    """

    req_model: ClassVar[type[PayloadBaseModel] | None] = None
    """Sorğunun payload model-i"""

    resp_model: ClassVar[Any] = dict
    """Sorğunun cavabının payload model-i"""

    dry: ClassVar[bool] = False
    """Simulasiya bool-u: True olarsa, sorğu göndərilmir, göndərilən data qaytarılır"""

    def __init__(
        self,
        req_model: Any = UNSET,
        resp_model: Any = UNSET,
        dry: Any = UNSET,
    ):
        """
        Args:
            req_model: Sorğunun payload model-i. Verilməsə, class atributu istifadə olunur.
            resp_model: Sorğunun cavabının payload model-i. Verilməsə, class atributu istifadə olunur.
            dry: Simulasiya bool-u. Verilməsə, class atributu istifadə olunur.
        """  # noqa: E501
        # Geriyə uyğunluq: dəyər `__init__`-ə ötürülübsə, instansiya səviyyəsində
        # class atributunu override edirik; əks halda ClassVar dəyəri qalır.
        if req_model is not UNSET:
            self.req_model = req_model
        if resp_model is not UNSET:
            self.resp_model = resp_model
        if dry is not UNSET:
            self.dry = dry

    def build_request_model(self, *args, **kwds) -> PayloadBaseModel | None:
        """Verilən argumentlərdən `self.req_model` instansiyasını yaradan funksiya.

        Model heç bir instansiya state-i saxlamadan qaytarılır (thread/async safe).
        """
        if self.req_model:
            return self.req_model.from_args(*args, **kwds)

        return None

    def set_urlparams(self, url: str, req_model: PayloadBaseModel | None = None) -> str:
        """URL-in query-param-larını set etmək üçün funksiya (əgər varsa)

        Args:
            url: Format olunmalı url
            req_model: `build_request_model`-dan qayıdan model instansiyası
        """
        if not (self.req_model and self.req_model.URL_PARAM_FIELDS and req_model):
            if any(tup[1] for tup in string.Formatter().parse(url) if tup[1] is not None):
                raise ValueError('URL should not expect any arguments')

            return url

        return url.format(
            **req_model.model_dump(
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

        Misal üçün: Bax [`EPointClientClass`](https://integrify.mmzeynalli.dev/integrations/epoint/api-reference/client/#integrify.epoint.client.EPointClientClass)
        """

    def handle_payload(self, req_model: PayloadBaseModel | None, *args, **kwds):
        """Verilən sorğu modelini payload-a (dict) çevirən funksiya.
        `self.req_model` qeyd edilməyibsə, bu funksiya override olunmalıdır (!).

        Args:
            req_model: `build_request_model`-dan qayıdan model instansiyası
        """
        if self.req_model and req_model is not None:
            return req_model.model_dump(
                by_alias=True,
                exclude=self.req_model.URL_PARAM_FIELDS,
                mode='json',
            )

        # `req_model` yoxdursa, o zaman `*args` boş olmalıdır, çünki onların key-ləri bilinmir
        assert not args

        return kwds

    def post_handle_payload(self, data: Any):
        """Sorğunun payload-ının post-processing-i. Əgər sorğu göndərməmişdən qabaq
        son datanın üzərinə əlavələr lazımdırsa, bu funksiyadan istifadə edə bilərsiniz.

        Misal üçün: Bax [`EPointClientClass`](https://integrify.mmzeynalli.dev/integrations/epoint/api-reference/client/#integrify.epoint.client.EPointClientClass)

        Args:
            data: `pre_handle_payload` və `handle_payload` funksiyalarından yaradılmış data.
        """
        return data  # pragma: no cover

    def handle_request(self, req_model: PayloadBaseModel | None, *args, **kwds):
        """Sorğu üçün payload-u hazırlayan funksiya. Üç mərhələ icra edir,
        və bu mərhələlər override oluna bilər. (Misal üçün:
        Bax [`EPointClientClass`](https://integrify.mmzeynalli.dev/integrations/epoint/api-reference/client/#integrify.epoint.client.EPointClientClass)

        1. Pre-processing
        2. Payload hazırlama
        3. Post-processing

        Args:
            req_model: `build_request_model`-dan qayıdan model instansiyası
        """
        pre_data = self.pre_handle_payload(*args, **kwds) or {}
        data = {**pre_data, **self.handle_payload(req_model, *args, **kwds)}
        return self.post_handle_payload(data)

    def handle_response(
        self,
        resp: httpx.Response,
    ) -> APIResponse[_ResponseT] | httpx.Response:
        """Sorğudan gələn cavab payload-ı handle edən funksiya. `self.resp_model` schema-sı
        verilibsə, onunla parse və validate olunur, əks halda, json/dict formatında qaytarılır.
        """
        if not self.resp_model:
            return resp

        return APIResponse[self.resp_model].model_validate(resp, from_attributes=True)


class APIExecutor:
    """API sorgularını icra edən class"""

    def __init__(
        self,
        name: str,
        sync: bool = True,
        dry: bool = False,
        timeout: float | None = DEFAULT_TIMEOUT,
    ):
        """
        Args:
            name: API klientin adı. Logging üçün istifadə olunur.
            sync: Sync (True) və ya Async (False) klient seçimi. Default olaraq sync seçilir.
            dry: Sorğu göndərmək əvəzinə göndəriləcək datanı qaytarmaq üçün istifadə olunur.
                    Debug üçün nəzərdə tutulub.
            timeout: httpx sorğu timeout-u (saniyə ilə).
        """
        self.sync = sync
        self.dry = dry
        self.timeout = timeout
        self.client_name = name
        self.logger = LOGGER_FUNCTION(name)

    @cached_property
    def client(self) -> httpx.Client | httpx.AsyncClient:
        """httpx sorğu client-i.

        Lazy yaradılır: import zamanı deyil, ilk sorğuda açılır. Beləliklə, `AsyncClient`
        event loop-dan kənarda import zamanı yaradılmır və heç istifadə olunmayan
        klient üçün socket açılmır.
        """
        if self.sync:
            return httpx.Client(timeout=self.timeout)

        return httpx.AsyncClient(timeout=self.timeout)

    def close(self) -> None:
        """Sync httpx client-in bağlanması (əgər yaradılıbsa)"""
        client = self.__dict__.get('client')
        if client is not None and isinstance(client, httpx.Client):
            client.close()
            del self.__dict__['client']

    async def aclose(self) -> None:
        """Async httpx client-in bağlanması (əgər yaradılıbsa)"""
        client = self.__dict__.get('client')
        if client is not None and isinstance(client, httpx.AsyncClient):
            await client.aclose()
            del self.__dict__['client']

    @property
    def request_function(
        self,
    ) -> Callable[
        [str, str, APIPayloadHandler, Any],  # input args
        httpx.Response
        | APIResponse[_ResponseT]
        | DryResponse
        | Coroutine[Any, Any, httpx.Response | APIResponse[_ResponseT] | DryResponse],  # output
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
        headers: dict | None = None,
        **kwds,
    ) -> httpx.Response | APIResponse[_ResponseT] | DryResponse:
        """Sync sorğu atan funksiya

        Args:
            url: Sorğunun full url-i
            verb: Sorğunun metodun (`POST`, `GET`, və s.)
            handler: Sorğu və cavabın payload handler-i
        """
        assert isinstance(self.client, httpx.Client)

        req_model = handler.build_request_model(*args, **kwds)
        data = handler.handle_request(req_model, *args, **kwds)
        full_headers = {**handler.headers, **(headers or {})}
        full_url = handler.set_urlparams(url, req_model)

        if self.dry or handler.dry:
            return DryResponse(
                url=full_url,
                verb=verb,
                request_args=handler.req_args,
                headers=full_headers,
                data=data,
            )

        request_kwds = {'headers': full_headers, **handler.req_args}

        if verb == 'GET':
            request_kwds['params'] = data
        else:
            request_kwds['json'] = data

        response = self.client.request(verb, full_url, **request_kwds)

        if not response.is_success:
            self.logger.error(
                '%s request to %s failed. Status code was %d. Content => %s',
                self.client_name,
                full_url,
                response.status_code,
                response.content.decode(errors='replace'),
            )

        return handler.handle_response(response)

    async def async_req(  # pragma: no cover
        self,
        url: str,
        verb: str,
        handler: APIPayloadHandler,
        *args,
        headers: dict | None = None,
        **kwds,
    ) -> httpx.Response | APIResponse[_ResponseT] | DryResponse:
        """Async sorğu atan funksiya

        Args:
            url: Sorğunun full url-i
            verb: Sorğunun metodun (`POST`, `GET`, və s.)
            handler: Sorğu və cavabın payload handler-i
        """
        assert isinstance(self.client, httpx.AsyncClient)

        req_model = handler.build_request_model(*args, **kwds)
        data = handler.handle_request(req_model, *args, **kwds)
        full_headers = {**handler.headers, **(headers or {})}
        full_url = handler.set_urlparams(url, req_model)

        if self.dry or handler.dry:
            # Sorğu göndərmək əvəzinə göndəriləcək datanı qaytarmaq
            return DryResponse(
                url=full_url,
                verb=verb,
                request_args=handler.req_args,
                headers=full_headers,
                data=data,
            )

        request_kwds = {'headers': full_headers, **handler.req_args}

        if verb == 'GET':
            request_kwds['params'] = data
        else:
            request_kwds['json'] = data

        response = await self.client.request(verb, full_url, **request_kwds)

        if not response.is_success:
            self.logger.error(
                '%s request to %s failed. Status code was %d. Content => %s',
                self.client_name,
                full_url,
                response.status_code,
                response.content.decode(errors='replace'),
            )

        return handler.handle_response(response)
