from decimal import Decimal
from typing import Optional

from pydantic import Field

from integrify.epoint import env
from integrify.schemas import PayloadBaseModel


class MinimalPaymentInputPayloadSchema(PayloadBaseModel):
    amount: Decimal
    currency: str
    order_id: str


class BasePaymentInputPayloadSchema(MinimalPaymentInputPayloadSchema):
    success_redirect_url: Optional[str] = env.EPOINT_SUCCESS_REDIRECT_URL
    error_redirect_url: Optional[str] = env.EPOINT_FAILED_REDIRECT_URL
    description: Optional[str] = None


##############################################################################
class PaymentInputPayloadSchema(BasePaymentInputPayloadSchema):
    other_attr: Optional[dict] = None


class GetTransactionStatusInputPayloadSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')


class SaveCardInputPayloadSchema(PayloadBaseModel):
    pass


class PayWithSavedCardInputPayloadSchema(MinimalPaymentInputPayloadSchema):
    card_id: str


class PayAndSaveCardInputPayloadSchema(BasePaymentInputPayloadSchema):
    pass


class PayoutInputPayloadSchema(MinimalPaymentInputPayloadSchema):
    card_id: str
    description: Optional[str] = None


class RefundInputPayloadSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')
    currency: str
    amount: Optional[Decimal] = None


class SplitPayInputPayloadSchema(BasePaymentInputPayloadSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    other_attr: Optional[dict] = None


class SplitPayWithSavedCardInputPayloadSchema(MinimalPaymentInputPayloadSchema):
    card_id: str
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: Optional[str] = None


class SplitPayAndSaveCardInputPayloadSchema(BasePaymentInputPayloadSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: Optional[str] = None
