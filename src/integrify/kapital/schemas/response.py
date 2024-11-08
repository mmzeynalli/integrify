from pydantic import BaseModel, Field


class CreateOrderResponseSchema(BaseModel):
    id: int
    password: str
    redirect_url: str


class OrderType(BaseModel):
    title: str


class OrderInformationResponseSchema(BaseModel):
    id: int
    type_rid: str = Field(alias='typeRid')
    status: str
    last_status_login: str = Field(alias='lastStatusLogin')
    amount: float
    currency: str
    create_time: str = Field(alias='createTime')
    type: OrderType
