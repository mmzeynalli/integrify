from decimal import Decimal
from typing import Optional

from pydantic import Field

from integrify.epoint import env
from integrify.schemas import PayloadBaseModel


class MinimalPaymentRequestSchema(PayloadBaseModel):
    amount: Decimal
    currency: str
    order_id: str


class BasePaymentRequestSchema(MinimalPaymentRequestSchema):
    success_redirect_url: Optional[str] = env.EPOINT_SUCCESS_REDIRECT_URL
    error_redirect_url: Optional[str] = env.EPOINT_FAILED_REDIRECT_URL
    description: Optional[str] = None


##############################################################################
class PaymentRequestSchema(BasePaymentRequestSchema):
    other_attr: Optional[dict] = None


class GetTransactionStatusRequestSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')


class SaveCardRequestSchema(PayloadBaseModel):
    pass


class PayWithSavedCardRequestSchema(MinimalPaymentRequestSchema):
    card_id: str


class PayAndSaveCardRequestSchema(BasePaymentRequestSchema):
    pass


class PayoutRequestSchema(MinimalPaymentRequestSchema):
    card_id: str
    description: Optional[str] = None


class RefundRequestSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')
    currency: str
    amount: Optional[Decimal] = None


class SplitPayRequestSchema(BasePaymentRequestSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    other_attr: Optional[dict] = None


class SplitPayWithSavedCardRequestSchema(MinimalPaymentRequestSchema):
    card_id: str
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: Optional[str] = None


class SplitPayAndSaveCardRequestSchema(BasePaymentRequestSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: Optional[str] = None
