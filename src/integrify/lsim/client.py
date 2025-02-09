from typing import TYPE_CHECKING, Optional

import httpx

from integrify.api import APIClient
from integrify.lsim import env
from integrify.lsim.handlers import (
    CheckBalancePayloadHandler,
    GetReportGetPayloadHandler,
    SendSMSGetPayloadHandler,
    SendSMSPostPayloadHandler,
)


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

    if TYPE_CHECKING:

        def get_report_get(self, tranid: int, login: Optional[str] = None) -> httpx.Response:
            """Yadda saxlanılmış kartla ödəniş sorğusu

            **Endpoint:** */api/1/execute-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay_with_saved_card(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx')
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.epoint.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
            cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir.

            Args:
                tranid: Ödəniş miqdarı. Numerik dəyər.
                login: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            """  # noqa: E501


LSIMClient = LSIMClientClass()
LSIMAsyncClient = LSIMClientClass(sync=False)
