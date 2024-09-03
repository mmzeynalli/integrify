from decimal import Decimal
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class EPointResponseStatus(StrEnum):
    SUCCESS = 'success'
    ERROR = 'error'
    FAILED = 'failed'


class EPointSaveCardResponseSchema(BaseModel):
    status: EPointResponseStatus
    message: Optional[str] = None
    # if success
    redirect_url: Optional[str] = None
    card_id: Optional[str] = None


class EPointPayWithSavedCardResponseSchema(BaseModel):
    status: EPointResponseStatus
    code: str
    message: str
    # if success
    transaction: Optional[str] = None
    bank_transaction: Optional[str] = None
    bank_response: Optional[str] = None
    card_name: Optional[str] = None
    card_mask: Optional[str] = None
    rrn: Optional[str] = None
    amount: Optional[Decimal] = None
