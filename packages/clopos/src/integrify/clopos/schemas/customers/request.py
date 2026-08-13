from typing import Literal

from pydantic import Field, model_serializer
from typing_extensions import TypedDict

from integrify.clopos.helpers import IsoDate
from integrify.clopos.schemas.common.request import PaginatedDataRequest
from integrify.clopos.schemas.enums import Gender
from integrify.schemas import PayloadBaseModel
from integrify.utils import UnsetField, UnsetOrNoneField


class CustomerFilter(TypedDict):
    by: Literal['name', 'phones', 'group_id']
    value: str


class GetCustomersRequest(PaginatedDataRequest):
    with_: UnsetField[list[Literal['group', 'balance', 'cashback_balance']]] = Field(exclude=True)
    filters: UnsetField[list[CustomerFilter]] = Field(exclude=True)

    @model_serializer()
    def serialize_model(self) -> dict:
        """Model serializer"""
        data = {}

        for i, with_item in enumerate(self.with_ or []):
            data[f'with[{i}]'] = with_item

        for i, filter_ in enumerate(self.filters or []):
            data[f'filters[{i}][0]'] = filter_['by']
            data[f'filter[{i}][1]'] = filter_['value']

        return data


class CreateCustomerRequest(PayloadBaseModel):
    name: str
    email: UnsetField[str]
    phone: UnsetField[str]
    code: UnsetField[str]
    cid: UnsetField[str]
    description: UnsetField[str]
    group_id: UnsetField[int]
    gender: UnsetOrNoneField[Gender]
    date_of_birth: UnsetField[IsoDate]
