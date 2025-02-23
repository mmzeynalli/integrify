from typing import TYPE_CHECKING, List

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
from integrify.utils import _UNSET, Unsettable

__all__ = ['PostaGuverciniClientClass']


class PostaGuverciniClientClass(APIClient):
    """Posta Guvercini sorğular üçün baza class"""

    def __init__(
        self,
        name='PostaGuvercini',
        base_url=env.API.BASE_URL,
        default_handler=None,
        sync=True,
        dry=False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

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
            send_date: Unsettable[str] = _UNSET,
            expire_date: Unsettable[str] = _UNSET,
            channel: Unsettable[str] = _UNSET,
            originator: Unsettable[str] = _UNSET,
            username: Unsettable[str] = _UNSET,
            password: Unsettable[str] = _UNSET,
        ) -> APIResponse[SendSingleSMSResponseSchema]:
            """Tək SMS göndərilməsi

            **Endpoint:** */api_json/v1/Sms/Send_1_N*

            Example:
                ```python
                from integrify.postaguvercini import PostaGuverciniRequest

                PostaGuverciniRequest.send_single_sms(
                    message="Test SMS",
                    receivers=["905320000000"],
                )
                ```

            **Cavab formatı**: [`SendSingleSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendSingleSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                message: SMS mətnini göstərir. Boş ola bilməz.
                receivers: SMS qəbul edənləri göstərir. Boş ola bilməz.
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                send_date: SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date: Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel: SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator: Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istənildikdə istifadə ediləcək bir sahədir. Göndəriləcək məlumat müştəri xidmətləri nümayəndəsi tərəfindən veriləcək və 11 simvol dəyərindədir.
            """  # noqa: E501

        def send_multiple_sms(
            self,
            messages: List[dict],
            send_date: Unsettable[str] = _UNSET,
            expire_date: Unsettable[str] = _UNSET,
            channel: Unsettable[str] = _UNSET,
            originator: Unsettable[str] = _UNSET,
            username: Unsettable[str] = _UNSET,
            password: Unsettable[str] = _UNSET,
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
            ```

            **Cavab formatı**: [`SendMultipleSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendMultipleSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                messages: SMS mətnini və qəbul edəni göstərir. Boş ola bilməz.
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                send_date: SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date: Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel: SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator: Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istən
            """  # noqa: E501

        def status(
            self,
            message_ids: List[str],
            username: Unsettable[str] = _UNSET,
            password: Unsettable[str] = _UNSET,
        ) -> APIResponse[StatusResponseSchema]:
            """SMS status sorğusu

            **Endpoint:** /api_json/v1/Sms/Status

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.status(message_ids=["123456"])
            ```

            **Cavab formatı**: [`StatusResponseSchema`][integrify.postaguvercini.schemas.response.StatusResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS statusu haqqında məlumat gəlir.

            Args:
                message_ids: SMS mesajlarının ID-ləri. Boş ola bilməz.
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def credit_balance(
            self,
            username: Unsettable[str] = _UNSET,
            password: Unsettable[str] = _UNSET,
        ) -> APIResponse[CreditBalanceResponseSchema]:
            """Kredit balans sorğusu

            **Endpoint:** /api_json/v1/Sms/CreditBalance

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.credit_balance()
            ```

            **Cavab formatı**: [`CreditBalanceResponseSchema`][integrify.postaguvercini.schemas.response.CreditBalanceResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq kredit balans məlumatı gəlir.

            Args:
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501


PostaGuverciniClient = PostaGuverciniClientClass(sync=True)
PostaGuverciniAsyncClient = PostaGuverciniClientClass(sync=False)
