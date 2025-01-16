from pydantic import field_validator

from integrify.kapital.schemas.enums import PMO_RESULT_CODES
from integrify.kapital.schemas.utils import BaseSchema


class Match(BaseSchema):
    tran_action_id: str
    rid_by_pmo: str


class FullReverseOrderResponseSchema(BaseSchema):
    match: Match
    pmo_result_code: str

    @field_validator('pmo_result_code', mode='before')
    @classmethod
    def pmo_result_code_to_msg(cls, v: str) -> str:
        """PMO kodunu mesaja çevirir."""
        return PMO_RESULT_CODES[v]


class RefundOrderResponseSchema(FullReverseOrderResponseSchema):
    approval_code: str


class ClearingOrderResponseSchema(FullReverseOrderResponseSchema):
    pass


class PartialReverseOrderResponseSchema(FullReverseOrderResponseSchema):
    pass
