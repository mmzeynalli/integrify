from integrify.kapitalbank.schemas.enums import TransactionStatus
from integrify.kapitalbank.schemas.utils import BaseSchema
from pydantic import computed_field


class CreateOrderResponseSchema(BaseSchema):
    id: int
    password: str
    hpp_url: str

    @computed_field
    @property
    def redirect_url(self) -> str:
        """Redirect url generasiyası"""
        return f'{self.hpp_url}?id={self.id}&password={self.password}'


class OrderType(BaseSchema):
    title: str


class OrderInformationResponseSchema(BaseSchema):
    id: int
    type_rid: str
    status: TransactionStatus
    last_status_login: str
    amount: float
    currency: str
    create_time: str
    type: OrderType
