from enum import Enum
from typing import TypeVar, Union

from pydantic import BaseModel

_ResponseT = TypeVar('_ResponseT', bound=Union[BaseModel, dict])
"""Dynamic response type."""

T = TypeVar('T')

_UNSET = object()
"""Unset arguments"""

Unsettable = Union[T, _UNSET]  # type: ignore[valid-type]
UnsettableAndNone = Union[T, _UNSET, None]  # type: ignore[valid-type]


class Environment(str, Enum):
    TEST = 'test'
    PROD = 'prod'
