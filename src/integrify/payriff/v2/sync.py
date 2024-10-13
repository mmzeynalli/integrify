from datetime import datetime
from decimal import Decimal
from typing import Optional

from integrify.base import ApiResponse, SyncApiRequest, send_request
from integrify.payriff import env
from integrify.payriff.schemas.types import PayriffMinimalResponse

__all__ = ['PayriffRequest']


class PayriffRequestClass(SyncApiRequest):
    """Payriff sorğular üçün baza class (v2)"""

    def __init__(self):
        super().__init__('Payriff', env.PAYRIFF_LOGGER_NAME)

        self.base_url = 'https://api.payriff.com/api/v2/'
        self.headers['Authorization'] = env.PAYRIFF_AUTHORIZATION_KEY
        self.body_data: dict = {}

    @send_request
    def invoice(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        expire_date: datetime | str,
        full_name: str,
        installment_period: int,
        installment_product_type: str,
        message: str,
        lang: Optional[str] = 'az',
        email: Optional[str] = None,
        phone: Optional[str] = None,
        send_sms: Optional[bool] = False,
        send_whatsapp: Optional[bool] = False,
        send_email: Optional[bool] = True,
        is_amount_dynamic: Optional[bool] = False,
        is_direct_pay: Optional[bool] = False,
        description: Optional[str] = None,
    ) -> ApiResponse[PayriffMinimalResponse]:
        self.path = env.V2_API.INVOICES
        self.verb = 'POST'
        self.resp_model = PayriffMinimalResponse

        if not phone and (send_sms or send_whatsapp):
            raise ValueError('Phone must be provided if send_sms or send_whatsapp is True')

        if not email and send_email:
            raise ValueError('Email must be provided if send_email is True')

        if isinstance(expire_date, datetime):
            expire_date = expire_date.isoformat()

        self.body_data.update(
            {
                'amount': amount,
                'currencyType': currency,
                'customMessage': message,
                'expireDate': expire_date,
                'fullName': full_name,
                'installmentPeriod': installment_period,
                'installmentProductType': installment_product_type,
                'languageType': lang,
                'sendSms': send_sms,
                'sendWhatsapp': send_whatsapp,
                'sendEmail': send_email,
                'amountDynamic': is_amount_dynamic,
                'directPay': is_direct_pay,
            }
        )

        if email:
            self.body_data['email'] = email

        if phone:
            self.body_data['phone'] = phone

        if description:
            self.body_data['description'] = description


PayriffRequest = PayriffRequestClass()
