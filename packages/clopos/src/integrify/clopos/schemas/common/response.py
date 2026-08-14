from typing import Generic, Literal, TypeVar

from integrify.utils import UnsetField
from pydantic import BaseModel

_ObjectTypeT = TypeVar('_ObjectTypeT', bound=BaseModel)


class BaseResponse(BaseModel):
    success: Literal[True]
    """Success status of the request"""

    message: UnsetField[str]
    """Success message"""

    time: int
    """Response time (ms)"""

    timestamp: str
    """ISO 8601 date"""

    unix: int
    """Unix timestamp of the response"""


class PaginatedResponse(BaseResponse):
    total: UnsetField[int]
    """Number of items returned"""

    sorts: UnsetField[list[str]]
    """List of sortable fields"""


class ObjectResponse(BaseResponse, Generic[_ObjectTypeT]):
    data: _ObjectTypeT
    """Object returned"""


class ObjectListResponse(PaginatedResponse, Generic[_ObjectTypeT]):
    data: list[_ObjectTypeT]


class Errors(BaseModel):
    message: str | None = None
    type: str | None = None
    exception: str | None = None
    code: int | None = None
    http_code: int | None = None


class ErrorResponse(BaseModel):
    success: Literal[False]
    error: list[Errors] = []
    message: str | None = None
