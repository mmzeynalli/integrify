from decimal import Decimal
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class EPointResponseStatus(StrEnum):
    SUCCESS = 'success'
    ERROR = 'error'
    FAILED = 'failed'


class EPointMinimalResponseSchema(BaseModel):
    status: EPointResponseStatus
    message: Optional[str] = None


class EPointRedirectResponseSchema(EPointMinimalResponseSchema):
    # if success
    redirect_url: Optional[str] = None
    card_id: Optional[str] = None


class EPointPayWithSavedCardResponseSchema(EPointMinimalResponseSchema):
    code: str
    # if success
    transaction: Optional[str] = None
    bank_transaction: Optional[str] = None
    bank_response: Optional[str] = None
    rrn: Optional[str] = None
    card_mask: Optional[str] = None
    card_name: Optional[str] = None
    amount: Optional[Decimal] = None


class EPointPayoutResponseSchema(EPointMinimalResponseSchema):
    # If success
    transaction: Optional[str] = None
    bank_transaction: Optional[str] = None
    bank_response: Optional[str] = None
    rrn: Optional[str] = None
    card_mask: Optional[str] = None
    card_name: Optional[str] = None
    amount: Optional[Decimal] = None
