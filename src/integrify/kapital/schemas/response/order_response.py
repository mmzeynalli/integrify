from pydantic import computed_field

from integrify.kapital.schemas.utils import BaseSchema


class CreateOrderResponseSchema(BaseSchema):
    id: int
    password: str
    hpp_url: str

    @computed_field(return_type=str)  # type: ignore[prop-decorator]
    @property
    def redirect_url(self) -> str:
        return f'{self.hpp_url}?id={self.id}&password={self.password}'


class OrderType(BaseSchema):
    title: str


class OrderInformationResponseSchema(BaseSchema):
    id: int
    type_rid: str
    status: str
    last_status_login: str
    amount: float
    currency: str
    create_time: str
    type: OrderType
