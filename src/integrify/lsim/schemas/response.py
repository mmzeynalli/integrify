from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    success_message: Optional[str] = None
    error_message: Optional[str] = None
    obj: Optional[int] = -1
    error_code: Optional[int] = None
