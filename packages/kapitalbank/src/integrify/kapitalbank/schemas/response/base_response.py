from typing import Generic

from integrify.kapitalbank.schemas.enums import ErrorCode
from integrify.kapitalbank.schemas.utils import BaseSchema
from integrify.schemas import _ResponseT


class ErrorResponseBodySchema(BaseSchema):
    error_code: ErrorCode
    error_description: str
    error_details: dict | None = None


class BaseResponseSchema(BaseSchema, Generic[_ResponseT]):
    error: ErrorResponseBodySchema | None = None
    """The error response body."""

    data: _ResponseT | None = None
    """The data response body."""
