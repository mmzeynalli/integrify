from typing import TYPE_CHECKING, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.azericard import env
from integrify.azericard.schemas.enums import TrType
from integrify.azericard.schemas.request import MInfo

__all__ = ['AzeriCardClientClass']


class AzeriCardClientClass(APIClient):
    """AzeriCard sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('AzeriCard', sync=sync)

        self.add_url(
            'auth',
            env.MPI_API.AUTHORIZATION,
            'POST',
            base_url=env.MPI_API.get_base_url(env.AZERICARD_ENV),
        )

    def authorization(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        merch_name: str,
        merch_url: str,
        backref: str,
        name: str,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        lang: Optional[str] = None,
        timestamp: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        self.auth(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            merch_name=merch_name,
            merch_url=merch_url,
            trtype=TrType.AUTHORAZATION,
            backref=backref,
            name=name,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            lang=lang,
            timestamp=timestamp,
            m_info=m_info,
        )

    def pre_authorization(
        self,
        amount: Numeric,
        currency: str,
        order: str,
        desc: str,
        merch_name: str,
        merch_url: str,
        backref: str,
        name: str,
        email: Optional[str] = None,
        country: Optional[str] = None,
        merch_gmt: Optional[str] = None,
        lang: Optional[str] = None,
        timestamp: Optional[str] = None,
        m_info: Optional[MInfo] = None,
    ):
        self.auth(
            amount=amount,
            currency=currency,
            order=order,
            desc=desc,
            merch_name=merch_name,
            merch_url=merch_url,
            trtype=TrType.PRE_AUTHORAZATION,
            backref=backref,
            name=name,
            email=email,
            country=country,
            merch_gmt=merch_gmt,
            lang=lang,
            timestamp=timestamp,
            m_info=m_info,
        )

    if TYPE_CHECKING:

        def auth(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            merch_name: str,
            merch_url: str,
            trtype: str,
            backref: str,
            name: str,
            email: Optional[str] = None,
            country: Optional[str] = None,
            merch_gmt: Optional[str] = None,
            lang: Optional[str] = None,
            timestamp: Optional[str] = None,
            m_info: Optional[MInfo] = None,
        ) -> APIResponse:
            """Ödəniş sorğusu

            **Endpoint:** *https://testmpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardRequest

                AzeriCardRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            **Cavab formatı**: [`AuthResponseSchema`][integrify.azericard.schemas.response.AuthResponseSchema]

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


AzeriCardRequest = AzeriCardClientClass(sync=True)
AzeriCardAsyncRequest = AzeriCardClientClass(sync=False)
