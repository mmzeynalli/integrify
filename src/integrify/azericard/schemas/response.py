from typing import Optional

from pydantic import Field

from integrify.azericard.schemas.common import AzeriCardDataSchema
from integrify.azericard.schemas.enums import Action


class AuthResponseSchema(AzeriCardDataSchema):
    action: Action
    """EGateway fəaliyyət kodu"""

    rc: str = Field(min_length=2, max_length=2)
    """Əməliyyat cavab kodu (ISO-8583 Sahə 39)"""

    approval: Optional[str] = Field(..., min_length=6, max_length=6)
    """Müştəri bankının təsdiq kodu (ISO-8583 Sahə 38). Kart idarəetmə sistemi
    tərəfindən təmin edilmədikdə boş ola bilər."""

    rrn: str = Field(min_length=12, max_length=12)
    """Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)"""

    int_ref: str = Field(min_length=1, max_length=128)
    """Elektron ticarət şlüzünün daxili istinad nömrəsi"""
