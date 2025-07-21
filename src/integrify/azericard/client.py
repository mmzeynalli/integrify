from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIPayloadHandler, APIResponse
from integrify.azericard import env
from integrify.azericard.handler import (
    AuthAndSavePayloadHandler,
    AuthConfirmPayloadHandler,
    AuthPayloadHandler,
    AuthWithSavedCardPayloadHandler,
    GetTransactionStatusPayloadHandler,
    TransferConfirmPayloadHandler,
    TransferStartPayloadHandler,
)
from integrify.azericard.schemas.enums import AuthorizationResponseType, AuthorizationType
from integrify.azericard.schemas.request.auth import MInfo
from integrify.azericard.schemas.response import (
    GetTransactionStatusResponseSchema,
    TransferConfirmResponseSchema,
    TransferDeclineResponseSchema,
)
from integrify.schemas import DryResponse
from integrify.utils import _UNSET, Unsettable


class AzeriCardClientClass(APIClient):
    """AzeriCard sorğular üçün baza class"""

    def __init__(
        self,
        name: str = 'AzeriCard',
        base_url: Optional[str] = None,
        default_handler: Optional[APIPayloadHandler] = None,
        sync: bool = True,
        dry: bool = False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url(
            'authorization',
            env.MpiAPI.AUTHORIZATION,
            'POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('authorization', AuthPayloadHandler)

        self.add_url(
            'finalize',
            env.MpiAPI.AUTHORIZATION,
            verb='POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('finalize', AuthConfirmPayloadHandler)

        self.add_url(
            'auth_and_save_card',
            env.MpiAPI.SAVE_CARD,
            verb='POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_and_save_card', AuthAndSavePayloadHandler)

        self.add_url(
            'auth_with_saved_card',
            env.MpiAPI.SAVE_CARD,
            verb='POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('auth_with_saved_card', AuthWithSavedCardPayloadHandler)

        self.add_url(
            'get_transaction_status',
            env.MpiAPI.AUTHORIZATION,
            verb='POST',
            base_url=env.MpiAPI.BASE_URL,
        )
        self.add_handler('get_transaction_status', GetTransactionStatusPayloadHandler)

        self.add_url('transfer_start', env.MtAPI.TRANSFER, verb='GET', base_url=env.MtAPI.BASE_URL)
        self.add_handler('transfer_start', TransferStartPayloadHandler)

        self.add_url(
            'transfer_confirm',
            env.MtAPI.TRANSFER_CONFIRM,
            verb='POST',
            base_url=env.MtAPI.BASE_URL,
        )
        self.add_handler('transfer_confirm', TransferConfirmPayloadHandler)

        self.add_url(
            'transfer_decline',
            env.MtAPI.TRANSFER_DECLINE,
            verb='POST',
            base_url=env.MtAPI.BASE_URL,
        )

    if TYPE_CHECKING:

        def authorization(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: AuthorizationType,
            merch_name: str = env.AZERICARD_MERCHANT_NAME,  # type: ignore[assignment]
            merch_url: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            terminal: str = env.AZERICARD_MERCHANT_ID,  # type: ignore[assignment]
            email: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            country: Unsettable[str] = _UNSET,
            merch_gmt: Unsettable[str] = _UNSET,
            backref: str = env.AZERICARD_CALLBACK_URL,  # type: ignore[assignment]
            timestamp: Union[datetime, str] = datetime.now(),
            lang: str = env.AZERICARD_INTERFACE_LANG,  # type: ignore[assignment]
            name: Unsettable[str] = _UNSET,
            m_info: Unsettable[MInfo] = _UNSET,
        ) -> DryResponse:
            """Ümumi Ödəniş/Pul Dondurma/Dondurulmanı sorğusu

            **Endpoint:** *https://{test}mpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient
                from integrify.azericard.schemas.enums import AuthorizationType

                AzeriCardClient.authorization(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype=AuthorizationType.FREEZE, name='Filankes')
                ```

            **Cavab formatı**: Yoxdur. Redirect baş verir, nəticə callback sorğusunda qayıdır.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta: (AZN)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                trtype: Tranzaksiya növü: 0 (Pre-Avtorizasiya əməliyyatı, pulu bloklamaq/dondurmaq) və ya  1 (Avtorizasiya əməliyyatı, birbaşa ödəniş)
                email: Bildirişlər üçün Email ünvan. Qeyd olunmuş sahə doldurulduğu halda Gateway email ünvanı müəyyən etmək üçün əməliyyat nəticəsi haqqında bildiriş göndərə bilər
                country: Merchant shop 2 simvollu ölkə kodu. Merchant sistemi Gateway serverin yerləşdiyi ölkədən fərqli ölkədə yerləşirsə qeyd olunmalıdır
                merch_gmt: Merchant-ın UTC/GMT vaxt zonası. Merchant sistemi Gateway serverin yerləşdiyi vaxt zonasından fərqli vaxt zonasında yerləşirsə qeyd olunmalıdır
                backref: Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
                lang: Dil seçimi
                name: Müştərinin adı (kartda göstərildiyi kimi)
                m_info: Əlavə məlumatlar. Məs: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}
            """  # noqa: E501

        def finalize(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            rrn: str,
            int_ref: str,
            trtype: AuthorizationResponseType,
            terminal: str = env.AZERICARD_MERCHANT_ID,  # type: ignore[assignment]
            timestamp: Union[datetime, str] = datetime.now(),
        ) -> DryResponse:
            """PreAuthorization (pulu bloklama) sorğusuna cavab və ya direkt ödənişi refund sorğusu

            **Endpoint:** *https://{test}mpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient
                from integrify.azericard.schemas.enums import AuthorizationResponseType

                AzeriCardClient.finalize(amount=100, currency='AZN', order='12345678', rrn='payment_rrn', int_ref='int_ref', trtype=AuthorizationResponseType.ACCEPT_PAYMENT)
                ```

            **Cavab formatı**:

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta: (AZN)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                rrn: Ödənişin RRN-i, Authorization sorğusuna response-da gəlir
                int_ref: Ödənişin referansı, Authorization sorğusuna response-da gəlir
                trtype: Tranzaksiya növü: 21 (Təsdiq), 22 (Geri qaytarma), 24 (Ləğv etmə, spesifik banklar üçün istifadə olunur)
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def auth_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: AuthorizationType,
            merch_name: str = env.AZERICARD_MERCHANT_NAME,  # type: ignore[assignment]
            merch_url: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            terminal: str = env.AZERICARD_MERCHANT_ID,  # type: ignore[assignment]
            email: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            country: Unsettable[str] = _UNSET,
            merch_gmt: Unsettable[str] = _UNSET,
            backref: str = env.AZERICARD_CALLBACK_URL,  # type: ignore[assignment]
            timestamp: Union[datetime, str] = datetime.now(),
            lang: str = env.AZERICARD_INTERFACE_LANG,  # type: ignore[assignment]
            name: Unsettable[str] = _UNSET,
            m_info: Unsettable[MInfo] = _UNSET,
        ) -> DryResponse:
            """Ümumi kartı saxlayaraq ödəniş sorğusu

            **Endpoint:** *https://{test}mpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient
                from integrify.azericard.schemas.enums import AuthorizationType

                AzeriCardClient.auth_and_save_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype=AuthorizationType.DIRECT, name='Filankes')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta: (AZN)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı, pulu bloklamaq/dondurmaq),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
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
            amount: Numeric,
            currency: str,
            order: str,
            desc: str,
            trtype: AuthorizationType,
            token: str,
            merch_name: str = env.AZERICARD_MERCHANT_NAME,  # type: ignore[assignment]
            merch_url: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            terminal: str = env.AZERICARD_MERCHANT_ID,  # type: ignore[assignment]
            email: str = env.AZERICARD_MERCHANT_EMAIL,  # type: ignore[assignment]
            country: Unsettable[str] = _UNSET,
            merch_gmt: Unsettable[str] = _UNSET,
            backref: str = env.AZERICARD_CALLBACK_URL,  # type: ignore[assignment]
            timestamp: Union[datetime, str] = datetime.now(),
            lang: str = env.AZERICARD_INTERFACE_LANG,  # type: ignore[assignment]
            name: Unsettable[str] = _UNSET,
            m_info: Unsettable[MInfo] = _UNSET,
        ) -> DryResponse:
            """Ümumi saxlanmış kart ilə Authurization sorğusu

            **Endpoint:** *https://{test}mpi.3dsecure.az/token/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient
                from integrify.azericard.schemas.enums import AuthorizationType

                AzeriCardClient.auth_with_saved_card(amount=100, currency='AZN', order='12345678', desc='Ödəniş', trype=AuthorizationType.DIRECT, name='Filankes', token='card-token')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Sifariş valyutası: 3 simvollu valyuta: (AZN)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                desc: Ödənişin təsviri/açıqlaması
                merch_name: Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)
                merch_url: Satıcının web site URL-i
                trtype: Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı, pulu bloklamaq/dondurmaq),Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)
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
            tran_trtype: Union[AuthorizationType, AuthorizationResponseType],
            order: str,
            terminal: str = env.AZERICARD_MERCHANT_ID,  # type: ignore[assignment]
            timestamp: Union[datetime, str] = datetime.now(),
        ) -> APIResponse[GetTransactionStatusResponseSchema]:
            """Bitmiş tranzaksiyanın statusunu alma sorğusu

            **Endpoint:** *https://{test}mpi.3dsecure.az/cgi-bin/cgi_link*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient
                from integrify.azericard.schemas.enums import AuthorizationType

                AzeriCardClient.get_transaction_status(tran_trtype=AuthorizationType.DIRECT, order='12345678')
                ```

            **Cavab formatı**: [`GetTransactionStatusResponseSchema`][integrify.azericard.schemas.response.GetTransactionStatusResponseSchema]

            Args:
                tran_trtype: Sorğu üçün orijinal əməliyyat növü, TRTYPE (Məsələn: 0, 1, 22, 24 və s.)
                order: Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur, terminal id üçün bir gün ərzində unikal olmalıdır
                terminal: Bank tərəfindən təyin edilmiş Merchant Terminal ID. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                timestamp: Merchant server-lə e-Gateway server arasında zaman fərqi 1 saatı aşmamalıdır, əks halda Gateway tranzaksiyaya imtina verəcək. Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def transfer_start(
            self,
            merchant: str,
            srn: str,
            amount: Numeric,
            cur: str,
            receiver_credentials: str,
            redirect_link: str,
        ) -> DryResponse:
            """User-ə ödəniş etmək sorğusu

            **Endpoint:** *https://{test}mt.3dsecure.az/payment/view*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient

                AzeriCardClient.transfer_start(merchant='MyMerchant', srn='12345678', amount=100, cur='944', receiver_credentials='Filankəsov Filankəs', redirect_link='my-redirect-api-for-user')
                ```

            **Cavab formatı**: Callback sorğu baş verir

            Args:
                merchant: Şirkət adı
                srn: Unikal əməliyyat nömrəsi
                amount: Ödəniş məbləği
                cur: Ödəniş valyutasının 3 rəqəmli kodu (944 - AZN)
                receiver_credentials: İstifadəçinin tam adı
                redirect_link: Əməliyyatın sonunda müştərini yönləndirmək istədiyiniz keçid linki
            """  # noqa: E501

        def transfer_confirm(
            self,
            merchant: str,
            srn: str,
            amount: Numeric,
            cur: str,
            timestamp: Union[datetime, str] = datetime.now(),
        ) -> APIResponse[TransferConfirmResponseSchema]:
            """User-ə ödənişi təsdiqləmək sorğusu

            **Endpoint:** *https://{test}mt.3dsecure.az/api/confirm*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient

                AzeriCardClient.transfer_confirm(merchant='MyMerchant', srn='12345678', amount=100, cur='944')
                ```

            **Cavab formatı**: [TransferConfirmResponseSchema][integrify.azericard.schemas.response.TransferConfirmResponseSchema]

            Args:
                merchant: Şirkət adı
                srn: Unikal əməliyyat nömrəsi
                amount: Ödəniş məbləği
                cur: Ödəniş valyutasının 3 rəqəmli kodu (944 - AZN)
                timestamp: Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501

        def transfer_decline(
            self,
            merchant: str,
            srn: str,
            amount: Numeric,
            cur: str,
            timestamp: Union[datetime, str] = datetime.now(),
        ) -> APIResponse[TransferDeclineResponseSchema]:
            """User-ə ödənişi imtina etmək sorğusu

            **Endpoint:** *https://{test}mt.3dsecure.az/api/decline*

            Example:
                ```python
                from integrify.azericard import AzeriCardClient

                AzeriCardClient.transfer_decline(merchant='MyMerchant', srn='12345678', amount=100, cur='944')
                ```

            **Cavab formatı**: [TransferDeclineResponseSchema][integrify.azericard.schemas.response.TransferDeclineResponseSchema]

            Args:
                merchant: Şirkət adı
                srn: Unikal əməliyyat nömrəsi
                amount: Ödəniş məbləği
                cur: Ödəniş valyutasının 3 rəqəmli kodu (944 - AZN)
                timestamp: Dəyər verilmədikdə, `now` avtomatik göndəriləcək
            """  # noqa: E501


AzeriCardClient = AzeriCardClientClass(sync=True)
AzeriCardAsyncClient = AzeriCardClientClass(sync=False)
