from typing import TypeVar, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_ResponsePayloadT = TypeVar('_ResponsePayloadT', bound=Union[BaseModel, dict])
"""Dinamik payload cavab tipi."""


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
