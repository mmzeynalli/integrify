from pydantic import Field

from integrify.kapital.schemas.response.detailed_order_response import SrcToken
from integrify.kapital.schemas.response.refund_response import RefundOrderResponseSchema
from integrify.kapital.schemas.utils import BaseSchema


class LinkCardTokenResponseSchema(BaseSchema):
    status: str
    cvv2_auth_status: str = Field(alias='cvv2AuthStatus')
    tds_v1_auth_status: str = Field(alias='tdsV1AuthStatus')
    tds_v2_auth_status: str = Field(alias='tdsV2AuthStatus')
    otp_aut_status: str
    src_token: SrcToken


class ProcessPaymentWithSavedCardResponseSchema(RefundOrderResponseSchema):
    pass
