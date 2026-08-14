from decimal import Decimal
from urllib.parse import parse_qsl

from integrify.epoint.schemas.response import BaseWithCodeSchema
from pydantic import BaseModel, model_validator


class CallbackDataSchema(BaseModel):
    """Raw və encoded callback data schema-sı"""

    data: str
    """Base64 formatında gələn data"""

    signature: str
    """EPOINT_PRIVATE_KEY"""

    @model_validator(mode='before')
    @classmethod
    def convert_str_to_dict(cls, data: bytes) -> dict:
        """Query string formatında gələn datanı düzgün formata çevirmək üçün funksiya"""
        return dict(parse_qsl(data.decode()))


class DecodedCallbackDataSchema(BaseWithCodeSchema):
    """Decode olunmuş callback data schema-sı"""

    order_id: str | None = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    card_id: str | None = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""

    split_amount: Decimal | None = None
    """İkinci istifadəçi üçün ödəniş məbləği."""

    other_attr: str | None = None
    """Əlavə göndərdiyiniz seçimlər"""
