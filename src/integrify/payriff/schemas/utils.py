from typing import TypeVar, Union

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_ResponsePayloadT = TypeVar('_ResponsePayloadT', bound=Union[BaseModel, dict])
"""Dinamik payload cavab tipi."""


class BaseCamelRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_camel))

class BaseCamelResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=to_camel))