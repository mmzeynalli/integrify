from enum import Enum
from typing import Literal, TypeVar, Union

from pydantic import BaseModel

_ResponseT = TypeVar('_ResponseT', bound=Union[BaseModel, dict])
"""Dynamic response type."""

T = TypeVar('T')

_UNSET = object()
"""Set olunmamış argument dəyəri"""

Unsettable = Union[T, Literal[_UNSET]]  # type: ignore[valid-type]
""" Optional argument tipi """

UnsettableAndNone = Union[T, Literal[_UNSET], None]  # type: ignore[valid-type]
"""None dəyəri ala bilən optional argument tipi"""


class Environment(str, Enum):
    TEST = 'test'
    PROD = 'prod'
