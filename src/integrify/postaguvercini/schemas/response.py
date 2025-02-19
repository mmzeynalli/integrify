from typing import Optional

from integrify.postaguvercini.schemas.utils import BaseSchema


class ResultSchema(BaseSchema):
    balance: int


class CreditBalanceResponseSchema(BaseSchema):
    status_code: int
    status_description: str
    result: Optional[ResultSchema]
