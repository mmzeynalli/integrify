from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from integrify.lsim.schemas.enums import Code


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    success_message: Optional[str] = None
    error_message: Optional[str] = None
    obj: Optional[int] = -1
    error_code: Code
