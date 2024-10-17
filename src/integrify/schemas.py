from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator

ResponseType = TypeVar('ResponseType', bound=BaseModel)


class APIResponse(BaseModel, Generic[ResponseType]):
    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: ResponseType = Field(validation_alias='content')
    """Cavab sorğusunun body-si"""

    @field_validator('body', mode='before')
    def convert_to_dict(cls, v: str | bytes | dict) -> dict:
        if isinstance(v, dict):  # in tests
            return v

        import json

        return json.loads(v)


class PayloadBaseModel(BaseModel):
    @classmethod
    def from_args(cls, *args, **kwds):
        return cls.model_validate({**{k: v for k, v in zip(cls.model_fields.keys(), args)}, **kwds})
