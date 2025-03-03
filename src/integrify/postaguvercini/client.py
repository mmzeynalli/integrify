from datetime import datetime
from typing import TYPE_CHECKING, Union

from integrify.api import APIClient
from integrify.postaguvercini import env
from integrify.postaguvercini.handlers import (
    CreditBalancePayloadHandler,
    SendMultipleSMSPayloadHandler,
    SendSingleSMSPayloadHandler,
    StatusPayloadHandler,
)
from integrify.postaguvercini.schemas.enums import ChannelType
from integrify.postaguvercini.schemas.request import SMSMessage
from integrify.postaguvercini.schemas.response import (
    CreditBalanceResponseSchema,
    SendSMSResponseSchema,
    StatusResponseSchema,
)
from integrify.schemas import APIResponse
from integrify.utils import _UNSET, Unsettable


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

        self.add_url('get_status', env.API.STATUS, verb='POST')
        self.add_handler('get_status', StatusPayloadHandler)

        self.add_url('credit_balance', env.API.CREDIT_BALANCE, verb='POST')
        self.add_handler('credit_balance', CreditBalancePayloadHandler)

    if TYPE_CHECKING:

        def send_single_sms(
            self,
            message: str,
            receivers: list[str],
            send_date: Unsettable[Union[str, datetime]] = _UNSET,
            expire_date: Unsettable[Union[str, datetime]] = _UNSET,
            channel: ChannelType = ChannelType.OTP,
            originator: Unsettable[str] = _UNSET,
            username: str = env.POSTA_GUVERCINI_USERNAME,  # type: ignore[assignment]
            password: str = env.POSTA_GUVERCINI_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[SendSMSResponseSchema]:
            """Tək SMS göndərilməsi

            **Endpoint:** */api_json/v1/Sms/Send_1_N*

            Example:
                ```python
                from integrify.postaguvercini import PostaGuverciniClient

                PostaGuverciniClient.send_single_sms(
                    message="Test SMS",
                    receivers=["905320000000"],
                )
                ```

            **Cavab formatı**: [`SendSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                message: SMS mətnini göstərir. Boş ola bilməz.
                receivers: SMS qəbul edənləri göstərir. Boş ola bilməz.
                send_date: SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date: Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel: SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator: Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istənildikdə istifadə ediləcək bir sahədir. Göndəriləcək məlumat müştəri xidmətləri nümayəndəsi tərəfindən veriləcək və 11 simvol dəyərindədir.
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def send_multiple_sms(
            self,
            messages: list[SMSMessage],
            send_date: Unsettable[Union[str, datetime]] = _UNSET,
            expire_date: Unsettable[Union[str, datetime]] = _UNSET,
            channel: ChannelType = ChannelType.OTP,
            originator: Unsettable[str] = _UNSET,
            username: str = env.POSTA_GUVERCINI_USERNAME,  # type: ignore[assignment]
            password: str = env.POSTA_GUVERCINI_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[SendSMSResponseSchema]:
            """Çoxlu SMS göndərilməsi

            **Endpoint:** /api_json/v1/Sms/Send_N_N

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniClient

            PostaGuverciniClient.send_multiple_sms(
                messages=[
                    {"receiver": "905320000000", "message": "Test SMS 1"},
                    {"receiver": "905320000001", "message": "Test SMS 2"},
                ],
            )
            ```

            **Cavab formatı**: [`SendSMSResponseSchema`][integrify.postaguvercini.schemas.response.SendSMSResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq SMS göndərilməsi haqqında məlumat gəlir.

            Args:
                messages: SMS mətnini və qəbul edəni göstərir. Boş ola bilməz.
                send_date: SMS göndərilmə vaxtını göstərir. Boş olduqda dərhal sms göndəriləcək. Format: `yyyyMMdd HH:mm`
                expire_date: Sonuncu dəfə SMS göndərilməyə cəhd ediləcəyini göstərir. Boş olduqda, sistem tərəfindən müəyyən edilmiş vaxt etibarlı olacaq. Format: `yyyyMMdd HH:mm`
                channel: SMS-in göndərən ilə hansı platformada (OTP və ya BULK) göndəriləcəyini göstərir. Misal: OTP.
                originator: Bu, tək hesabla müxtəlif göndəricilər altında sms göndərmək istən
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_status(
            self,
            message_ids: list[str],
            username: str = env.POSTA_GUVERCINI_USERNAME,  # type: ignore[assignment]
            password: str = env.POSTA_GUVERCINI_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[StatusResponseSchema]:
            """SMS status sorğusu

            **Endpoint:** /api_json/v1/Sms/Status

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniClient

            PostaGuverciniClient.get_status(message_ids=["123456"])
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
            username: str = env.POSTA_GUVERCINI_USERNAME,  # type: ignore[assignment]
            password: str = env.POSTA_GUVERCINI_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[CreditBalanceResponseSchema]:
            """Kredit balans sorğusu

            **Endpoint:** /api_json/v1/Sms/CreditBalance

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniClient

            PostaGuverciniClient.credit_balance()
            ```

            **Cavab formatı**: [`CreditBalanceResponseSchema`][integrify.postaguvercini.schemas.response.CreditBalanceResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq kredit balans məlumatı gəlir.

            Args:
                username: Posta Guvercini hesabı adı. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: Posta Guvercini hesabı şifrəsi. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501


PostaGuverciniClient = PostaGuverciniClientClass(sync=True)
PostaGuverciniAsyncClient = PostaGuverciniClientClass(sync=False)
