from typing import Generic, Optional

from integrify.kapital.schemas.enums import ErrorCode
from integrify.kapital.schemas.utils import BaseSchema
from integrify.schemas import _ResponseT


class ErrorResponseBodySchema(BaseSchema):
    error_code: ErrorCode
    error_description: str


class BaseResponseSchema(BaseSchema, Generic[_ResponseT]):
    error: Optional[ErrorResponseBodySchema] = None
    """The error response body."""

    data: Optional[_ResponseT] = None
    """The data response body."""
