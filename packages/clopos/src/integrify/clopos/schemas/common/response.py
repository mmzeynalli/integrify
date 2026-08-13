from typing import Generic, Literal, Optional, TypeVar

from pydantic import BaseModel

from integrify.utils import UnsetField

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
    message: Optional[str] = None
    type: Optional[str] = None
    exception: Optional[str] = None
    code: Optional[int] = None
    http_code: Optional[int] = None


class ErrorResponse(BaseModel):
    success: Literal[False]
    error: list[Errors] = []
    message: Optional[str] = None
