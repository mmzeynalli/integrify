from integrify.lsim.single.schemas.enums import Code
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseGetResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    success_message: str | None = None
    """Uğurlu sorğu zamanı alınan mesaj"""

    error_message: str | None = None
    """Xəta mesajı"""

    obj: int | None = -1
    """Sorğudan asılı olaraq, bu field-in mənası dəyişir."""

    error_code: Code | None = None
    """Status kodu (həm uğurlu, həm xəta)"""


class BasePostResponseSchema(BaseGetResponseSchema):
    error_code: str | None = None
    """Status mesajı (həm uğurlu, həm xəta)"""


class ReportGetResponseSchema(BaseModel):
    error_code: Code | None = None
    """Status kodu (həm uğurlu, həm xəta)"""


class ReportPostResponseSchema(BaseModel):
    message: str | None = None
    """Xəta/uğur mesajı"""

    delivery_status: str | None = None
    """SMS Statusu"""
