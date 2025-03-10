from pydantic import Field

from integrify.payriff.schemas.response import BaseResponseSchema


class RefundResponseSchema(BaseResponseSchema):
    payload: None = Field(default=None, exclude=True)
