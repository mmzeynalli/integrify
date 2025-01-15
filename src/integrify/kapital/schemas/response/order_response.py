from pydantic import computed_field

from integrify.kapital.schemas.enums import TransactionStatus
from integrify.kapital.schemas.utils import BaseSchema


class CreateOrderResponseSchema(BaseSchema):
    id: int
    password: str
    hpp_url: str

    @computed_field  # type: ignore[prop-decorator]
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
