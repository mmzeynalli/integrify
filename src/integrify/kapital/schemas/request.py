from pydantic import Field
from decimal import Decimal
from typing import Optional, List
from integrify.kapital import env
from integrify.schemas import PayloadBaseModel


class CreateOrderDetails(PayloadBaseModel):
    # TODO: Update to decimal
    amount: str
    currency: str
    description: str
    language: Optional[str] = env.KAPITAL_INTERFACE_LANG
    redirect_url: Optional[str] = Field(
        alias="hppRedirectUrl", default=env.KAPITAL_REDIRECT_URL
    )
    order_type: Optional[str] = Field(alias="typeRid", default="Order_SMS")
    capture_purposes: Optional[List[str]] = Field(
        alias="hppCofCapturePurposes", default=["Cit"]
    )


class CreateOrderRequestSchema(PayloadBaseModel):
    order: CreateOrderDetails
