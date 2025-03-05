from datetime import datetime
from typing import TYPE_CHECKING, Union

from integrify.api import APIClient
from integrify.lsim import env as base_env
from integrify.lsim.single import env
from integrify.lsim.single.handlers import (
    CheckBalancePayloadHandler,
    GetReportGetPayloadHandler,
    GetReportPostPayloadHandler,
    SendSMSGetPayloadHandler,
    SendSMSPostPayloadHandler,
)
from integrify.lsim.single.schemas.response import (
    BaseGetResponseSchema,
    BasePostResponseSchema,
    ReportGetResponseSchema,
    ReportPostResponseSchema,
)
from integrify.schemas import APIResponse


class LSIMSingleSMSClientClass(APIClient):
    def __init__(
        self,
        name='LSIM',
        base_url=env.API.BASE_URL,
        default_handler=None,
        sync=True,
        dry=False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('send_sms_get', env.API.SEND_SMS_GET, verb='GET')
        self.add_handler('send_sms_get', SendSMSGetPayloadHandler)

        self.add_url('send_sms_post', env.API.SEND_SMS_POST, verb='POST')
        self.add_handler('send_sms_post', SendSMSPostPayloadHandler)

        self.add_url('check_balance', env.API.CHECK_BALANCE, verb='GET')
        self.add_handler('check_balance', CheckBalancePayloadHandler)

        self.add_url('get_report_get', env.API.GET_REPORT_GET, verb='GET')
        self.add_handler('get_report_get', GetReportGetPayloadHandler)

        self.add_url('get_report_post', env.API.GET_REPORT_POST, verb='POST')
        self.add_handler('get_report_post', GetReportPostPayloadHandler)

    if TYPE_CHECKING:

        def send_sms_get(
            self,
            msisdn: str,
            text: str,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
            sender: str = base_env.LSIM_SENDER_NAME,  # type: ignore[assignment]
            unicode: bool = False,
        ) -> APIResponse[BaseGetResponseSchema]:
            """SMS göndərən GET sorğusu

            **Endpoint:** */quicksms/v1/send*

            Example:
                ```python
                from integrify.lsim import LSIMSingleSMSClient

                LSIMSingleSMSClient.send_sms_get(msidn='99450XXXXXXX', text='test')
                ```

            Cavab formatı: [`BaseGetResponseSchema`][integrify.lsim.single.schemas.response.BaseGetResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseGetResponseSchema` formatında
            cavab gəlir, və uğurlu olduqda, `obj` field-ində transaction_id dəyəri gəlir.

            Args:
                msisdn: SMS göndəriləcək nömrə: ölkə kodu + operator kodu + nömrə: 99450XXXXXXX
                text: Mesaj məzmunu
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                sender: LSIM tərəfindən təyin olunmuş göndərən adınız. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                unicode: Mesajın unicode olub/olmaması. Əgər mesajda unikod simvollar (`ə`, `ş`, `ü` və s.) istifadə
                    edirsizsə, `True` seçməlisiniz
            """  # noqa: E501

        def send_sms_post(
            self,
            msisdn: str,
            text: str,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
            sender: str = base_env.LSIM_SENDER_NAME,  # type: ignore[assignment]
            unicode: bool = False,
            scheduled: Union[str, datetime] = 'NOW',
        ) -> APIResponse[BasePostResponseSchema]:
            """SMS göndərən POST sorğusu

            **Endpoint:** */quicksms/v1/smssender*

            Example:
                ```python
                from integrify.lsim import LSIMSingleSMSClient

                LSIMSingleSMSClient.send_sms_post(msidn='99450XXXXXXX', text='test')
                ```

            Cavab formatı: [`BasePostResponseSchema`][integrify.lsim.single.schemas.response.BasePostResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BasePostResponseSchema` formatında
            cavab gəlir, və uğurlu olduqda, `obj` field-ində transaction_id dəyəri gəlir.

            Args:
                msisdn: SMS göndəriləcək nömrə: ölkə kodu + operator kodu + nömrə: 99450XXXXXXX
                text: Mesaj məzmunu
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                sender: LSIM tərəfindən təyin olunmuş göndərən adınız. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                unicode: Mesajın unicode olub/olmaması. Əgər mesajda unikod simvollar (`ə`, `ş`, `ü` və s.) istifadə
                    edirsizsə, `True` seçməlisiniz
                scheduled: Öncədən SMS göndərilməsi üçün seçilmiş zaman. Zamanı `2023-05-19 15:40:05`
                    formatında verməlisiniz. Sahə boş qaldıqda, SMS sorğu atdığınız an gedəcək.
            """  # noqa: E501

        def check_balance(
            self,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[BaseGetResponseSchema]:
            """LSIM balans sorğusu

            **Endpoint:** */quicksms/v1/balance*

            Example:
                ```python
                from integrify.lsim import LSIMSingleSMSClient

                LSIMSingleSMSClient.check_balance()
                ```

            Cavab formatı: [`BaseGetResponseSchema`][integrify.lsim.single.schemas.response.BaseGetResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseGetResponseSchema` formatında
            cavab gəlir, `obj` field-ində balans dəyəri gəlir.

            Args:
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_report_get(
            self,
            trans_id: int,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
        ) -> APIResponse[ReportGetResponseSchema]:
            """Göndərilmiş SMS-in reportunu alan GET sorğusu

            **Endpoint:** */quicksms/v1/report*

            Example:
                ```python
                from integrify.lsim import LSIMSingleSMSClient

                LSIMSingleSMSClient.get_report_get(trans_id=1)
                ```

            Cavab formatı: [`ReportGetResponseSchema`][integrify.lsim.single.schemas.response.ReportGetResponseSchema]

            Args:
                trans_id: Uğurlu SMS göndərildikdə alınan transaction id
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_report_post(
            self,
            trans_id: int,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
        ) -> APIResponse[ReportPostResponseSchema]:
            """Göndərilmiş SMS-in reportunu alan POST sorğusu

            **Endpoint:** */quicksms/v1/smsreporter*

            Example:
                ```python
                from integrify.lsim import LSIMSingleSMSClient

                LSIMSingleSMSClient.get_report_post(trans_id=1)
                ```

            Cavab formatı: [`ReportPostResponseSchema`][integrify.lsim.single.schemas.response.ReportPostResponseSchema]

            Args:
                trans_id: Uğurlu SMS göndərildikdə alınan transaction id
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501


LSIMSingleSMSClient = LSIMSingleSMSClientClass()
LSIMSingleSMSAsyncClient = LSIMSingleSMSClientClass(sync=False)
