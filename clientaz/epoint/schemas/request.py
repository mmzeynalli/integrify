from typing import Optional
from urllib.parse import parse_qsl

from pydantic import BaseModel, model_validator


class EPointCallbackDataSchema(BaseModel):
    data: str
    signature: str

    @model_validator(mode='before')
    @classmethod
    def convert_str_to_dict(cls, data: bytes) -> dict:
        return dict(parse_qsl(data.decode()))


class EPointDecodedCallbackDataSchema(BaseModel):
    order_id: Optional[str] = None
    status: Optional[str] = None
    code: Optional[str] = None
    card_id: Optional[str] = None
    message: Optional[str] = None
    transaction: Optional[str] = None
    bank_transaction: Optional[str] = None
    bank_response: Optional[str] = None
    operation_code: Optional[str] = None
    rrn: Optional[str] = None
    card_name: Optional[str] = None
    card_mask: Optional[str] = None
    amount: Optional[str] = None
    other_attr: Optional[str] = None
