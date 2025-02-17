from typing import TYPE_CHECKING, Optional

from integrify.api import APIClient
from integrify.lsim import env
from integrify.lsim.handlers import (
    CheckBalancePayloadHandler,
    GetReportGetPayloadHandler,
    GetReportPostPayloadHandler,
    SendSMSGetPayloadHandler,
    SendSMSPostPayloadHandler,
)
from integrify.lsim.schemas.response import (
    BaseResponseSchema,
    ReportGetResponseSchema,
    ReportPostResponseSchema,
)
from integrify.schemas import APIResponse


class LSIMClientClass(APIClient):
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
            login: Optional[str] = None,
            password: Optional[str] = None,
            sender: Optional[str] = None,
            unicode: bool = False,
        ) -> APIResponse[BaseResponseSchema]:
            """SMS göndərən GET sorğusu

            **Endpoint:** */quicksms/v1/send*

            Example:
                ```python
                from integrify.lsim import LSIMClient

                LSIMClient.send_sms_get(msidn='99450123456', text='test')
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.lsim.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
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
            login: Optional[str] = None,
            password: Optional[str] = None,
            sender: Optional[str] = None,
            unicode: bool = False,
            scheduled: str = 'NOW',
        ) -> APIResponse[BaseResponseSchema]:
            """SMS göndərən POST sorğusu

            **Endpoint:** */quicksms/v1/smssender*

            Example:
                ```python
                from integrify.lsim import LSIMClient

                LSIMClient.send_sms_post(msidn='99450123456', text='test')
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.lsim.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
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
            login: Optional[str] = None,
            password: Optional[str] = None,
        ) -> APIResponse[BaseResponseSchema]:
            """LSIM balans sorğusu

            **Endpoint:** */quicksms/v1/balance*

            Example:
                ```python
                from integrify.lsim import LSIMClient

                LSIMClient.check_balance()
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.lsim.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
            cavab gəlir, `obj` field-ində balans dəyəri gəlir.

            Args:
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_report_get(
            self,
            trans_id: int,
            login: Optional[str] = None,
        ) -> APIResponse[ReportGetResponseSchema]:
            """Göndərilmiş SMS-in reportunu alan GET sorğusu

            **Endpoint:** */quicksms/v1/report*

            Example:
                ```python
                from integrify.lsim import LSIMClient

                LSIMClient.get_report_get(trans_id=1)
                ```

            Cavab formatı: [`ReportGetResponseSchema`][integrify.lsim.schemas.response.ReportGetResponseSchema]

            Args:
                trans_id: Uğurlu SMS göndərildikdə alınan transaction id
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_report_post(
            self,
            trans_id: int,
            login: Optional[str] = None,
        ) -> APIResponse[ReportPostResponseSchema]:
            """Göndərilmiş SMS-in reportunu alan POST sorğusu

            **Endpoint:** */quicksms/v1/smsreporter*

            Example:
                ```python
                from integrify.lsim import LSIMClient

                LSIMClient.get_report_post(trans_id=1)
                ```

            Cavab formatı: [`ReportPostResponseSchema`][integrify.lsim.schemas.response.ReportPostResponseSchema]

            Args:
                trans_id: Uğurlu SMS göndərildikdə alınan transaction id
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501


LSIMClient = LSIMClientClass()
LSIMAsyncClient = LSIMClientClass(sync=False)
