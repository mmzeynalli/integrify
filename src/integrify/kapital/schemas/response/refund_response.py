from integrify.kapital.schemas.utils import BaseSchema


class Match(BaseSchema):
    tran_action_id: str
    rid_by_pmo: str


class RefundOrderResponseSchema(BaseSchema):
    approval_code: str
    match: Match
    pmo_result_code: str


class FullReverseOrderResponseSchema(BaseSchema):
    match: Match
    pmo_result_code: str


class ClearingOrderResponseSchema(FullReverseOrderResponseSchema):
    pass


class PartialReverseOrderResponseSchema(FullReverseOrderResponseSchema):
    pass
