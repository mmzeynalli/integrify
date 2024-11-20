from typing import Generic, Optional

from integrify.kapital.schemas.utils import BaseSchema
from integrify.schemas import ResponseType


class ErrorResponseBodySchema(BaseSchema):
    error_code: str
    error_description: str


class BaseResponseSchema(BaseSchema, Generic[ResponseType]):
    error: Optional[ErrorResponseBodySchema] = None
    """The error response body."""

    data: Optional[ResponseType] = None
    """The data response body."""
