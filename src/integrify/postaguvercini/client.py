from typing import TYPE_CHECKING, List, Optional

from integrify.api import APIClient
from integrify.postaguvercini import env
from integrify.postaguvercini.handlers import (
    CreditBalancePayloadHandler,
    SendMultipleSMSPayloadHandler,
    SendSingleSMSPayloadHandler,
    StatusPayloadHandler,
)
from integrify.postaguvercini.schemas.response import (
    CreditBalanceResponseSchema,
    SendMultipleSMSResponseSchema,
    SendSingleSMSResponseSchema,
    StatusResponseSchema,
)
from integrify.schemas import APIResponse

__all__ = ['PostaGuverciniClientClass']


class PostaGuverciniClientClass(APIClient):
    """Posta Guvercini sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('PostaGuvercini', env.API.BASE_URL, None, sync=sync)

        self.add_url('send_single_sms', env.API.SEND_SINGLE_SMS, verb='POST')
        self.add_handler('send_single_sms', SendSingleSMSPayloadHandler)

        self.add_url('send_multiple_sms', env.API.SEND_MULTIPLE_SMS, verb='POST')
        self.add_handler('send_multiple_sms', SendMultipleSMSPayloadHandler)

        self.add_url('status', env.API.STATUS, verb='POST')
        self.add_handler('status', StatusPayloadHandler)

        self.add_url('credit_balance', env.API.CREDIT_BALANCE, verb='POST')
        self.add_handler('credit_balance', CreditBalancePayloadHandler)

    if TYPE_CHECKING:

        def send_single_sms(
            self,
            message: str,
            receivers: List[str],
            send_date: Optional[str] = None,
            expire_date: Optional[str] = None,
            channel: Optional[str] = None,
            originator: Optional[str] = None,
        ) -> APIResponse[SendSingleSMSResponseSchema]:
            """Tək SMS göndərilməsi

            **Endpoint:** /api_json/v1/Sms/Send_1_N

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.send_single_sms(
                message="Test SMS",
                receivers=["905320000000"],
            )
            ``

            **Cavab formatı**: [`SendSingleSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendSingleSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                message (str): SMS mətnini göstərir. Boş ola bilməz.
                receivers (List[str]): SMS qəbul edənləri göstərir. Boş ola bilməz.
                send_date (Optional[str]): SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date (Optional[str]): Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel (Optional[str]): SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator (Optional[str]): Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istənildikdə istifadə ediləcək bir sahədir. Göndəriləcək məlumat müştəri xidmətləri nümayəndəsi tərəfindən veriləcək və 11 simvol dəyərindədir.
            """  # noqa: E501

        def send_multiple_sms(
            self,
            messages: List[dict],
            send_date: Optional[str] = None,
            expire_date: Optional[str] = None,
            channel: Optional[str] = None,
            originator: Optional[str] = None,
        ) -> APIResponse[SendMultipleSMSResponseSchema]:
            """Çoxlu SMS göndərilməsi

            **Endpoint:** /api_json/v1/Sms/Send_N_N

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.send_multiple_sms(
                messages=[
                    {"receiver": "905320000000", "message": "Test SMS 1"},
                    {"receiver": "905320000001", "message": "Test SMS 2"},
                ],
            )
            ``

            **Cavab formatı**: [`SendMultipleSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendMultipleSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                messages (List[dict]): SMS mətnini və qəbul edəni göstərir. Boş ola bilməz.
                send_date (Optional[str]): SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date (Optional[str]): Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel (Optional[str]): SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator (Optional[str]): Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istən
            """  # noqa: E501

        def status(self, message_ids: List[str]) -> APIResponse[StatusResponseSchema]:
            """SMS status sorğusu

            **Endpoint:** /api_json/v1/Sms/Status

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.status(message_ids=["123456"])
            ``

            **Cavab formatı**: [`StatusResponseSchema`][integrify.postaguvercini.schemas.response.StatusResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS statusu haqqında məlumat gəlir.

            Args:
                message_ids (List[str]): SMS mesajlarının ID-ləri. Boş ola bilməz.
            """  # noqa: E501

        def credit_balance(self) -> APIResponse[CreditBalanceResponseSchema]:
            """Kredit balans sorğusu

            **Endpoint:** /api_json/v1/Sms/CreditBalance

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.credit_balance()
            ``

            **Cavab formatı**: [`CreditBalanceResponseSchema`][integrify.postaguvercini.schemas.response.CreditBalanceResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq kredit balans məlumatı gəlir.

            Args:
                None
            """  # noqa: E501


PostaGuverciniRequest = PostaGuverciniClientClass(sync=True)
PostaGuverciniAsyncRequest = PostaGuverciniClientClass(sync=False)
