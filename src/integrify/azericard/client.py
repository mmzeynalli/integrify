from datetime import datetime  # pylint: disable=unused-argument
from typing import TYPE_CHECKING
from typing import SupportsFloat as Numeric

# pylint: disable=unused-argument
from integrify.api import APIClient, APIResponse
from integrify.azericard import env
from integrify.azericard.handler import (
    AuthAndSavePayloadHandler,
    AuthConfirmPayloadHandler,
    AuthPayloadHandler,
    AuthWithSavedCardPayloadHandler,
    ConfirmTransactionPayloadHandler,
    GetTransactionStatusPayloadHandler,
    StartTransferPayloadHandler,
)
from integrify.azericard.schemas.enums import TrType
from integrify.azericard.schemas.request import MInfo  # pylint: disable=unused-argument
from integrify.azericard.schemas.response import GetTransactionStatusResponseSchema
from integrify.schemas import DryResponse
from integrify.utils import _UNSET, Unsettable


class AzeriCardClientClass(APIClient):
    """AzeriCard sorğular üçün baza class"""

    def __init__(self, sync: bool = True, dry: bool = False):
        super().__init__('AzeriCard', sync=sync, dry=dry)

        self.add_url('auth', env.MpiAPI.AUTHORIZATION, 'POST', base_url=env.MpiAPI.BASE_URL)
        self.add_handler('auth', AuthPayloadHandler)

        self.add_url(
            'auth_response',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_response', AuthConfirmPayloadHandler)

        self.add_url(
            'auth_and_save_card',
            env.MpiAPI.SAVE_CARD,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_and_save_card', AuthAndSavePayloadHandler)

        self.add_url(
            'auth_with_saved_card',
            env.MpiAPI.SAVE_CARD,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_with_saved_card', AuthWithSavedCardPayloadHandler)

        self.add_url(
            'get_transaction_status',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('get_transaction_status', GetTransactionStatusPayloadHandler)

        self.add_url('start_transfer', env.MtAPI.TRANSFER, 'POST', env.MtAPI.BASE_URL)
        self.add_handler('start_transfer', StartTransferPayloadHandler)

        self.add_url('confirm_transfer', env.MtAPI.TRANSFER_CONFIRM, 'POST', env.MtAPI.BASE_URL)
        self.add_handler('confirm_transfer', ConfirmTransactionPayloadHandler)

    # arguments are given for sake of type-hinting. None is needed to NOT SEND unset variables
    # to pydantic model in order to trigger default values.
    def pay(  # pylint: disable=duplicate-code
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ) -> DryResponse:
        """Ödəniş sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay(amount=100, currency='944', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501
        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth(trtype=TrType.AUTHORAZATION, **kwds)

    def pay_and_save_card(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ) -> DryResponse:
        """Ödəniş və kartı yadda saxlama sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay_and_save_card(amount=100, currency='944', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Saxlamalı olduğunuz kartın ID-si də callback-də gəlir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_and_save_card(trtype=TrType.AUTHORAZATION, **kwds)

    def pay_with_saved_card(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        token: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Yadda saxlanılmış kartla ödəniş sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay_and_save_card(amount=100, currency='944', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            token: Yadda saxlanılmış kartın ID-si. Save-card sorğularında callback-də gəlir.
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_with_saved_card(trtype=TrType.AUTHORAZATION, **kwds)

    def block(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Pul Bloklama/Dondurma sorğusu.

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block(amount=100, currency='944', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth(trtype=TrType.PRE_AUTHORAZATION, **kwds)

    def block_and_save_card(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Pul bloklama/dondurma və kartı yadda saxlama sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block_and_save_card(amount=100, currency='944', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Saxlamalı olduğunuz kartın ID-si də callback-də gəlir. Həmçinin, bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_and_save_card(trtype=TrType.PRE_AUTHORAZATION, **kwds)

    def block_with_saved_card(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        desc: str,  # pylint: disable=unused-argument
        token: str,  # pylint: disable=unused-argument
        merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Yadda saxlanılmış kartdan pulu bloklama/dondurma sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block_with_saved_card(amount=100, currency='944', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            token: Yadda saxlanılmış kartın ID-si. Save-card sorğularında callback-də gəlir.
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            name: Müştərinin adı (kartda göstərildiyi kimi)
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_with_saved_card(trtype=TrType.PRE_AUTHORAZATION, **kwds)

    def accept_blocked_payment(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        rrn: str,  # pylint: disable=unused-argument
        int_ref: str,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Blok olunmuş məbləği qəbul etmək sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.accept_blocked_payment(amount=100, currency='944', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul etmək üçün gönmdərmək lazımdır

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_response(trtype=TrType.ACCEPT_REQUEST, **kwds)

    def reverse_blocked_payment(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        rrn: str,  # pylint: disable=unused-argument
        int_ref: str,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Blok olunmuş məbləği qəbul ETMƏMƏK (online) sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.reverse_blocked_payment(amount=100, currency='944', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul ETMƏMƏK üçün gönmdərmək lazımdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_response(trtype=TrType.RETURN_REQUEST, **kwds)

    def cancel_blocked_payment(
        self,
        amount: Numeric,  # pylint: disable=unused-argument
        currency: str,  # pylint: disable=unused-argument
        order: str,  # pylint: disable=unused-argument
        rrn: str,  # pylint: disable=unused-argument
        int_ref: str,  # pylint: disable=unused-argument
        terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
        timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
    ):
        """Blok olunmuş məbləği qəbul ETMƏMƏK (offline) sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.cancel_blocked_payment(amount=100, currency='944', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul ETMƏMƏK üçün gönmdərmək lazımdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501

        kwds = {k: v for k, v in locals().items() if k != 'self'}
        return self.auth_response(trtype=TrType.CANCEL_REQUEST, **kwds)

    if TYPE_CHECKING:

        def auth(
            self,
            amount: Numeric,  # pylint: disable=unused-argument
            currency: str,  # pylint: disable=unused-argument
            order: str,  # pylint: disable=unused-argument
            desc: str,  # pylint: disable=unused-argument
            trtype: TrType,
            merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
            lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """Ümumi Ödəniş/Pul Dondurma/Dondurulmanı tamamlama sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth(amount=100, currency='944', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
                ```

            **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                lang: Dil seçimi
                name: Müştərinin adı (kartda göstərildiyi kimi)
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def auth_response(
            self,
            amount: Numeric,  # pylint: disable=unused-argument
            currency: str,  # pylint: disable=unused-argument
            order: str,  # pylint: disable=unused-argument
            rrn: str,  # pylint: disable=unused-argument
            int_ref: str,  # pylint: disable=unused-argument
            trtype: TrType,
            terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """PreAuthorization sorğusuna cavab sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_response(amount=100, currency='944', order='12345678', rrn='payment_rrn', int_ref='int_ref', trtype='21')
                ```

            **Cavab formatı**:

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                rrn: Ödənişin RRN-i, Authorization sorğusuna response-da gəlir
                int_ref: Ödənişin referansı, Authorization sorğusuna response-da gəlir
                trtype: Tranzaksiya növü = 21 (Təsdiq), Tranzaksiya növü = 22 (Geri qaytarma), Tranzaksiya növü = 24 (Ləğv etmə)
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def auth_and_save_card(
            self,
            amount: Numeric,  # pylint: disable=unused-argument
            currency: str,  # pylint: disable=unused-argument
            order: str,  # pylint: disable=unused-argument
            desc: str,  # pylint: disable=unused-argument
            trtype: TrType,
            merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
            lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """Ümumi kartı saxlayaraq ödəniş sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_and_save_card(amount=100, currency='944', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                lang: Dil seçimi
                name: Müştərinin adı (kartda göstərildiyi kimi)
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def auth_with_saved_card(
            self,
            amount: Numeric,  # pylint: disable=unused-argument
            currency: str,  # pylint: disable=unused-argument
            order: str,  # pylint: disable=unused-argument
            desc: str,  # pylint: disable=unused-argument
            trtype: TrType,
            token: str,  # pylint: disable=unused-argument
            merch_name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_url: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            terminal: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            email: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            country: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            merch_gmt: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            backref: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
            lang: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            name: Unsettable[str] = _UNSET,  # pylint: disable=unused-argument
            m_info: Unsettable[MInfo] = _UNSET,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """Ümumi saxlanmış kart ilə Authurization sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_with_saved_card(amount=100, currency='944', order='12345678', desc='Ödəniş', trype='1', name='Filankes', token='card-token')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 rəqəmli valyuta kodu (AZN - 944)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                token: Yadda saxlanılmış kartın ID-si
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                lang: Dil seçimi
                name: Müştərinin adı (kartda göstərildiyi kimi)
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def get_transaction_status(
            self,
            tran_trtype: TrType,
            order: str,  # pylint: disable=unused-argument
            terminal: Unsettable[str],  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime],  # pylint: disable=unused-argument
        ) -> APIResponse[GetTransactionStatusResponseSchema]:
            """Bitmiş tranzaksiyanın statusunu alma sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.get_transaction_status(tran_trtype='21', order='12345678')
                ```

            **Cavab formatı**: [`GetTransactionStatusResponseSchema`][integrify.azericard.schemas.response.GetTransactionStatusResponseSchema]

            Args:
                tran_trtype: Sorğu üçün orijinal əməliyyat növü (Məsələn: TRTYPE 0, 1, 22, 24 və s.)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def start_transfer(
            self,
            merchant: str,  # pylint: disable=unused-argument
            srn: str,  # pylint: disable=unused-argument
            amount: Numeric,  # pylint: disable=unused-argument
            cur: str,  # pylint: disable=unused-argument
            receiver_credentials: str,  # pylint: disable=unused-argument
            redirect_link: str,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """User-ə ödəniş etmək sorğusu

            **Endpoint:** *https://testmt.3dsecure.az/payment/view*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.start_transfer(merchant='MyMerchant', srn='12345678', amount=100, cur='944', receiver_credentials='Filankəsov Filankəs', redirect_link='my-redirect-api-for-user')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                merchant: Şirkət adı
                srn: Unikal əməliyyat nömrəsi
                amount: Ödəniş məbləği
                cur: Ödəniş valyutası
                receiver_credentials: İstifadəçinin tam adı
                redirect_link: Əməliyyatın sonunda müştərini yönləndirmək istədiyiniz keçid linki
            """  # noqa: E501

        def confirm_transfer(
            self,
            merchant: str,  # pylint: disable=unused-argument
            srn: str,  # pylint: disable=unused-argument
            amount: Numeric,  # pylint: disable=unused-argument
            cur: str,  # pylint: disable=unused-argument
            timestamp: Unsettable[datetime] = _UNSET,  # pylint: disable=unused-argument
        ) -> DryResponse:
            """User-ə ödənişi təsdiqləmək sorğusu

            **Endpoint:** *https://testmt.3dsecure.az/api/confirm*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.confirm_transfer(merchant='MyMerchant', srn='12345678', amount=100, cur='944')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                merchant: Şirkət adı
                srn: Unikal əməliyyat nömrəsi
                amount: Ödəniş məbləği
                cur: Ödəniş valyutası
                timestamp: Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501


AzeriCardClient = AzeriCardClientClass(sync=True)
AzeriCardAsyncClient = AzeriCardClientClass(sync=False)
