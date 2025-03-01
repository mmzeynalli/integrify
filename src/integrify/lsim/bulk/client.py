from typing import TYPE_CHECKING

from integrify.api import APIClient
from integrify.lsim import env as base_env
from integrify.lsim.bulk import env
from integrify.lsim.bulk.handlers import (
    GetBalancePayloadHandler,
    GetBulkSMSDeatiledReportPayloadHandler,
    GetBulkSMSDeatiledWithDateReportPayloadHandler,
    GetBulkSMSReportPayloadHandler,
    SendBulkSMSDifferentMessagesPayloadHandler,
    SendBulkSMSOneMessagePayloadHandler,
)
from integrify.lsim.bulk.schemas.response import (
    GetBalanceResponseSchema,
    GetBulkSMSDetailedReportResponseSchema,
    GetBulkSMSReportResponseSchema,
    SendBulkSMSResponseSchema,
)
from integrify.schemas import APIResponse


class LSIMBulkSMSClientClass(APIClient):
    def __init__(
        self,
        name='LSIM-BulkSMS',
        base_url=env.API.BASE_URL,
        default_handler=None,
        sync=True,
        dry=False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('bulk_send_one_message', env.API.ENDPOINT, verb='POST')
        self.add_handler('bulk_send_one_message', SendBulkSMSOneMessagePayloadHandler)

        self.add_url('bulk_send_different_messages', env.API.ENDPOINT, verb='POST')
        self.add_handler('bulk_send_different_messages', SendBulkSMSDifferentMessagesPayloadHandler)

        self.add_url('get_report', env.API.ENDPOINT, verb='POST')
        self.add_handler('get_report', GetBulkSMSReportPayloadHandler)

        self.add_url('get_detailed_report', env.API.ENDPOINT, verb='POST')
        self.add_handler('get_detailed_report', GetBulkSMSDeatiledReportPayloadHandler)

        self.add_url('get_detailed_report_with_dates', env.API.ENDPOINT, verb='POST')
        self.add_handler(
            'get_detailed_report_with_dates',
            GetBulkSMSDeatiledWithDateReportPayloadHandler,
        )

        self.add_url('check_balance', env.API.ENDPOINT, verb='POST')
        self.add_handler('check_balance', GetBalancePayloadHandler)

    if TYPE_CHECKING:

        def bulk_send_one_message(
            self,
            controlid: int,
            msisdns: list[str],
            bulkmessage: str,
            scheduled: str = 'NOW',
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
            title: str = base_env.LSIM_SENDER_NAME,  # type: ignore[assignment]
        ) -> APIResponse[SendBulkSMSResponseSchema]:
            """Bir SMS-i toplu şəkildə bir çox nəfərə göndərmək sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.bulk_send_one_message(controlid=1, msisdns=['99450XXXXXXX'], bulkmessage='Hello world')
                ```

            Cavab formatı: [`SendBulkSMSResponseSchema`][integrify.lsim.bulk.schemas.response.SendBulkSMSResponseSchema]

            Args:
                controlid: Unikal sorğu id-si. Siz tərəfdən generasiya olunur.
                msisdns: SMS göndəriləcək nömrələr listi. Hər nömrə bu formatda olmalıdır: ölkə kodu + operator kodu + nömrə: 99450XXXXXXX
                bulkmessage: Bu nömrələrə göndəriləcək mesaj məzmunu
                scheduled: Öncədən SMS göndərilməsi üçün seçilmiş zaman. Zamanı `2023-05-19 15:40:05`
                    formatında verməlisiniz. Sahə boş qaldıqda, SMS sorğu atdığınız an gedəcək.
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                title: LSIM tərəfindən təyin olunmuş göndərən adınız. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def bulk_send_different_messages(
            self,
            controlid: int,
            msisdns: list[str],
            messages: list[str],
            scheduled: str = 'NOW',
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
            title: str = base_env.LSIM_SENDER_NAME,  # type: ignore[assignment]
        ) -> APIResponse[SendBulkSMSResponseSchema]:
            """Toplu şəkildə bir çox nəfərə fərqli SMS göndərmək sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.bulk_send_one_message(controlid=1, msisdns=['99450XXXXXXX', '99451XXXXXXX'],
                                                        messages=['Hello world 1', 'Hello world 2'])
                ```

            Cavab formatı: [`SendBulkSMSResponseSchema`][integrify.lsim.bulk.schemas.response.SendBulkSMSResponseSchema]

            Args:
                controlid: Unikal sorğu id-si. Siz tərəfdən generasiya olunur.
                msisdns: SMS göndəriləcək nömrələr listi. Hər nömrə bu formatda olmalıdır: ölkə kodu + operator kodu + nömrə: 99450XXXXXXX
                messages: Bu nömrələrə göndəriləcək mesajların düzgün ardıcıllıqla məzmunu
                scheduled: Öncədən SMS göndərilməsi üçün seçilmiş zaman. Zamanı `2023-05-19 15:40:05`
                    formatında verməlisiniz. Sahə boş qaldıqda, SMS sorğu atdığınız an gedəcək.
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                title: LSIM tərəfindən təyin olunmuş göndərən adınız. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_report(
            self,
            taskid: int,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[GetBulkSMSReportResponseSchema]:
            """Toplu göndərilmiş SMSlərin report sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.get_report(taskid=1)
                ```

            Cavab formatı: [`GetBulkSMSReportResponseSchema`][integrify.lsim.bulk.schemas.response.GetBulkSMSReportResponseSchema]

            Args:
                taskid: Uğurlu toplu SMS göndərdikdə alınmış taskid.
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_detailed_report(
            self,
            taskid: int,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[GetBulkSMSDetailedReportResponseSchema]:
            """Toplu göndərilmiş SMSlərin detallı report sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.get_detailed_report(taskid=1)
                ```

            Cavab formatı: [`GetBulkSMSDetailedReportResponseSchema`][integrify.lsim.bulk.schemas.response.GetBulkSMSDetailedReportResponseSchema]

            Args:
                taskid: Uğurlu toplu SMS göndərdikdə alınmış taskid.
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def get_detailed_report_with_dates(
            self,
            taskid: int,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[GetBulkSMSDetailedReportResponseSchema]:
            """Toplu göndərilmiş SMSlərin detallı report (+ tarix) sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.get_detailed_report_with_dates(taskid=1)
                ```

            Cavab formatı: [`GetBulkSMSDetailedReportResponseSchema`][integrify.lsim.bulk.schemas.response.GetBulkSMSDetailedReportResponseSchema]

            Args:
                taskid: Uğurlu toplu SMS göndərdikdə alınmış taskid.
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501

        def check_balance(
            self,
            login: str = base_env.LSIM_LOGIN,  # type: ignore[assignment]
            password: str = base_env.LSIM_PASSWORD,  # type: ignore[assignment]
        ) -> APIResponse[GetBalanceResponseSchema]:
            """Balansı öyrənmək sorğusu

            **Endpoint:** */smxml/api*

            Example:
                ```python
                from integrify.lsim import LSIMBulkSMSClient

                LSIMBulkSMSClient.check_balance()
                ```

            Cavab formatı: [`GetBalanceResponseSchema`][integrify.lsim.bulk.schemas.response.GetBalanceResponseSchema]

            Args:
                login: LSIM logininiz.  Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
                password: LSIM parolunuz. Mühit dəyişəni kimi təyin olunmayıbsa, burada parametr kimi ötürülməlidir.
            """  # noqa: E501


LSIMBulkSMSClient = LSIMBulkSMSClientClass()
LSIMBulkSMSAsyncClient = LSIMBulkSMSClientClass(sync=False)
