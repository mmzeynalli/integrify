from typing import TYPE_CHECKING, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.azericard import env
from integrify.azericard.handler import (
    AuthConfirmPayloadHandler,
    AuthPayloadHandler,
    GetTransactionStatusPayloadHandler,
    PayAndSavePayloadHandler,
    PayWithSavedCardPayloadHandler,
)
from integrify.azericard.schemas.enums import TrType
from integrify.azericard.schemas.request import MInfo
from integrify.azericard.schemas.response import GetTransactionStatusResponseSchema

__all__ = ['AzeriCardAsyncRequest', 'AzeriCardClientClass', 'AzeriCardRequest']


class AzeriCardClientClass(APIClient):
    """AzeriCard sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('AzeriCard', sync=sync)

        self.add_url(
            'auth',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth', AuthPayloadHandler)

        self.add_url(
            'auth_resp',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_resp', AuthConfirmPayloadHandler)

        self.add_url(
            'auth_and_save_card',
            env.MpiAPI.SAVE_CARD,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_and_save_card', PayAndSavePayloadHandler)

        self.add_url(
            'auth_with_saved_card',
            env.MpiAPI.SAVE_CARD,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_with_saved_card', PayWithSavedCardPayloadHandler)

        self.add_url(
            'get_transaction_status',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('get_transaction_status', GetTransactionStatusPayloadHandler)

    def pay(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Ödəniş sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay(amount=100, currency='AZN', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        return self.auth(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.AUTHORAZATION,
            name=name,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def pay_and_save_card(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Ödəniş və kartı yadda saxlama sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay_and_save_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Saxlamalı olduğunuz kartın ID-si də callback-də gəlir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501
        return self.auth_and_save_card(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.AUTHORAZATION,
            name=name,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def pay_with_saved_card(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        card_token: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Yadda saxlanılmış kartla ödəniş sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.pay_and_save_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            card_token: Yadda saxlanılmış kartın ID-si. Save-card sorğularında callback-də gəlir.
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501

        return self.auth_with_saved_card(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.AUTHORAZATION,
            name=name,
            token=card_token,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def block(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Pul Bloklama/Dondurma sorğusu.

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block(amount=100, currency='AZN', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501
        return self.auth(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.PRE_AUTHORAZATION,
            name=name,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def block_and_save_card(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Pul bloklama/dondurma və kartı yadda saxlama sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block_and_save_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', name='Filankes')
            ```

        **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

        Saxlamalı olduğunuz kartın ID-si də callback-də gəlir. Həmçinin, bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501
        return self.auth_and_save_card(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.PRE_AUTHORAZATION,
            name=name,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def block_with_saved_card(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        name: str,
        card_token: str,
        merch_name: Optional[str] = None,
        merch_url: Optional[str] = None,
        terminal: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        backref: Optional[str] = None,
        timestamp: Optional[str] = None,
        lang: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        """Yadda saxlanılmış kartdan pulu bloklama/dondurma sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.block_with_saved_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu istifadə etdikdə, user-in ödəyəcəyi pul onun kartında bloklanır/dondurlur, amma çıxmır. Bir neçə müddət sonra,
        [`accept_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.accept_blocked_payment],
        [`reverse_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.reverse_blocked_payment],
        [`cancel_blocked_payment`][integrify.azericard.client.AzeriCardClientClass.cancel_blocked_payment] funksiyalarını çağırmaqla
        tranzaksiyanı bitirməlisiniz.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            desc: Ödənişin təsviri/açıqlaması
            name: Müştərinin adı (kartda göstərildiyi kimi)
            card_token: Yadda saxlanılmış kartın ID-si. Save-card sorğularında callback-də gəlir.
            merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır). Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            merch_url: Satıcının web site URL-i. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
            country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
            merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
            backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            lang: Dil seçimi
            m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
        """  # noqa: E501
        return self.auth_with_saved_card(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            trtype=TrType.PRE_AUTHORAZATION,
            name=name,
            token=card_token,
            merch_name=merch_name,
            merch_url=merch_url,
            terminal=terminal,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            backref=backref,
            timestamp=timestamp,
            lang=lang,
            m_info=m_info,
        )

    def accept_blocked_payment(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        rrn: str,
        int_ref: str,
        timestamp: Optional[str] = None,
    ):
        """Blok olunmuş məbləği qəbul etmək sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.accept_blocked_payment(amount=100, currency='AZN', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul etmək üçün gönmdərmək lazımdır

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501
        return self.auth_response(
            amount=amount,
            currency=currency,
            order=order,
            rrn=rrn,
            int_ref=int_ref,
            trtype=TrType.ACCEPT_REQUEST,
            timestamp=timestamp,
        )

    def reverse_blocked_payment(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        rrn: str,
        int_ref: str,
        timestamp: Optional[str] = None,
    ):
        """Blok olunmuş məbləği qəbul ETMƏMƏK (online) sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.reverse_blocked_payment(amount=100, currency='AZN', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul ETMƏMƏK üçün gönmdərmək lazımdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501
        return self.auth_response(
            amount=amount,
            currency=currency,
            order=order,
            rrn=rrn,
            int_ref=int_ref,
            trtype=TrType.RETURN_REQUEST,
            timestamp=timestamp,
        )

    def cancel_blocked_payment(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        rrn: str,
        int_ref: str,
        timestamp: Optional[str] = None,
    ):
        """Blok olunmuş məbləği qəbul ETMƏMƏK (offline) sorğusu

        **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

        Example:
            ```python
            from integrify.azericard import AzeriCardRequest

            AzeriCardRequest.cancel_blocked_payment(amount=100, currency='AZN', order='12345678', rrn='RRN', int_ref='INT_REF')
            ```

        **Cavab formatı**: Callback sorğu baş verir

        Bu sorğunu [`block`][integrify.azericard.client.AzeriCardClientClass.block] və bənzəri soröulardan
        sonra, ödənişi qəbul ETMƏMƏK üçün gönmdərmək lazımdır.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Sifariş valyutası: 3 simvollu valyuta kodu
            order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
            rrn: Merchant bank üzrə axraş sorğu nömrəsi (ISO-8583 Field 37). İlk sorğunun callback-ində gəlir.
            int_ref: Daxili E-Commercegateway sorğu nömrə. İlk sorğunun callback-ində gəlir.
            timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
        """  # noqa: E501
        return self.auth_response(
            amount=amount,
            currency=currency,
            order=order,
            rrn=rrn,
            int_ref=int_ref,
            trtype=TrType.CANCEL_REQUEST,
            timestamp=timestamp,
        )

    if TYPE_CHECKING:

        def auth(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: TrType,
            name: str,
            merch_name: Optional[str] = None,
            merch_url: Optional[str] = None,
            terminal: Optional[str] = None,
            email: Optional[str] = None,
            country: Optional[str] = None,
            merch_gmt: Optional[str] = None,
            backref: Optional[str] = None,
            timestamp: Optional[str] = None,
            lang: Optional[str] = None,
            m_info: Optional[MInfo] = None,
        ) -> APIResponse:
            """Ümumi Ödəniş/Pul Dondurma/Dondurulmanı tamamlama sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
                ```

            **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta kodu
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                name: Müştərinin adı (kartda göstərildiyi kimi)
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                lang: Dil seçimi
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def auth_response(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            rrn: str,
            int_ref: str,
            trtype: TrType,
            timestamp: Optional[str] = None,
        ) -> APIResponse[dict]:
            """PreAuthorization sorğusuna cavab sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_response(amount=100, currency='AZN', order='12345678', rrn='payment_rrn', int_ref='int_ref', trtype='21')
                ```

            **Cavab formatı**:

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta kodu
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                rrn: Ödənişin RRN-i, Authorization sorğusuna response-da gəlir
                int_ref: Ödənişin referansı, Authorization sorğusuna response-da gəlir
                trtype: Tranzaksiya növü = 21 (Təsdiq), Tranzaksiya növü = 22 (Geri qaytarma), Tranzaksiya növü = 24 (Ləğv etmə)
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def auth_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: TrType,
            name: str,
            merch_name: Optional[str] = None,
            merch_url: Optional[str] = None,
            terminal: Optional[str] = None,
            email: Optional[str] = None,
            country: Optional[str] = None,
            merch_gmt: Optional[str] = None,
            backref: Optional[str] = None,
            timestamp: Optional[str] = None,
            lang: Optional[str] = None,
            m_info: Optional[MInfo] = None,
        ) -> APIResponse[dict]:
            """Ümumi kartı saxlayaraq ödəniş sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_and_save_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype='1', name='Filankes')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta kodu
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                name: Müştərinin adı (kartda göstərildiyi kimi)
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                lang: Dil seçimi
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def auth_with_saved_card(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: TrType,
            name: str,
            token: str,
            merch_name: Optional[str] = None,
            merch_url: Optional[str] = None,
            terminal: Optional[str] = None,
            email: Optional[str] = None,
            country: Optional[str] = None,
            merch_gmt: Optional[str] = None,
            backref: Optional[str] = None,
            timestamp: Optional[str] = None,
            lang: Optional[str] = None,
            m_info: Optional[MInfo] = None,
        ) -> APIResponse[dict]:
            """Ümumi saxlanmış kart ilə Authurization sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.auth_with_saved_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype='1', name='Filankes', token='card-token')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta kodu
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                name: Müştərinin adı (kartda göstərildiyi kimi)
                token: Yadda saxlanılmış kartın ID-si
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                lang: Dil seçimi
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def get_transaction_status(
            self,
            tran_trtype: TrType,
            order: str,
            terminal: Optional[str],
            timestamp: Optional[str],
        ) -> APIResponse[GetTransactionStatusResponseSchema]:
            """Bitmiş tranzaksiyanın statusunu alma sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.get_transaction_status(tran_trtype='21', order='12345678')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                tran_trtype:
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def remit(self):
            """User-ə ödəniş etmək sorğusu"""


AzeriCardRequest = AzeriCardClientClass(sync=True)
AzeriCardAsyncRequest = AzeriCardClientClass(sync=False)
