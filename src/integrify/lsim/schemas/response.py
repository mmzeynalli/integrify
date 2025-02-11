from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from integrify.lsim.schemas.enums import Code


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    success_message: Optional[str] = None
    """Uğurlu sorğu zamanı alınan mesaj"""

    error_message: Optional[str] = None
    """Xəta mesajı"""

    obj: Optional[int] = -1
    """Sorğudan asılı olaraq, bu field-in mənası dəyişir."""

    error_code: Code
    """Status kodu (həm uğurlu, həm xəta)"""
