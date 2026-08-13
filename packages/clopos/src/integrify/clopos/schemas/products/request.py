from typing import Literal, Union

from pydantic import Field, field_serializer, model_serializer
from typing_extensions import NotRequired, TypedDict

from integrify.api import PayloadBaseModel
from integrify.clopos.helpers import BoolInt
from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.enums import ProductType
from integrify.utils import UnsetField


class GetProducstRequestFilter(TypedDict):
    type: NotRequired[list[ProductType]]
    """Filters by product type. Possible values: GOODS, DISH, TIMER, PREPARATION, INGREDIENT"""

    category_id: NotRequired[list[int]]
    """Lists products belonging to the specified category IDs"""

    station_id: NotRequired[list[int]]
    """Retrieves products assigned to the specified station IDs"""

    tags: NotRequired[list[int]]
    """Filters for products with the specified tag IDs"""

    giftable: NotRequired[BoolInt]
    """Filters for products that are ("1") or are not giftable"""

    discountable: NotRequired[BoolInt]
    """Filters for products that are ("1") or are not discountable"""

    inventory_behavior: NotRequired[int]
    """Filters by inventory behavior mode (e.g., "3")"""

    have_ingredients: NotRequired[BoolInt]
    """Retrieves products that have a recipe/ingredients ("1")"""

    sold_by_portion: NotRequired[BoolInt]
    """Lists products sold by portion ("1")"""

    has_variants: NotRequired[BoolInt]
    """Lists products that have variants (`modifications`) ("1")"""

    has_modifiers: NotRequired[BoolInt]
    """Lists products that have modifier group (`modificator_groups`) ("1")"""

    has_barcode: NotRequired[BoolInt]
    """Retrieves products that have a barcode ("1")"""

    has_service_charge: NotRequired[BoolInt]
    """Lists products to which a service charge applies ("1")"""


class GetProductsRequest(PaginatedDataRequest):
    selects: UnsetField[Union[list[str], str]] = Field(serialization_alias='selects[]')
    filters: UnsetField[GetProducstRequestFilter]

    @field_serializer('selects')
    def serialize_selects(self, value):
        """Transform to comma-separated string"""
        if isinstance(value, str):
            return value
        return ','.join(value)

    @field_serializer('filters')
    def serialize_filters(self, filters):
        """Transform to [field_name, value] format"""
        result = {}
        for key, value in filters.items():
            if value is not None:  # Only include non-None values
                result[key] = [key, value]

        return result


class GetProductByIDRequest(ByIDRequest):
    with_: UnsetField[
        list[
            Literal[
                'taxes',
                'unit',
                'modifications',
                'modificator_groups',
                'recipe',
                'packages',
                'media',
                'tags',
                'setting',
            ]
        ]
    ] = Field(serialization_alias='with[]')


class StopListFilter(TypedDict):
    by: Literal['id', 'limit', 'timestamp']
    from_: int
    to: NotRequired[int]


class GetStopListRequest(PayloadBaseModel):
    filters: UnsetField[list[StopListFilter]]

    @model_serializer
    def serialize_model(self) -> dict:
        """Model serializer"""
        data = {}

        for i, filter_ in enumerate(self.filters or []):
            data[f'filters[{i}][0]'] = filter_['by']
            data[f'filters[{i}][1][0]'] = filter_['from_']

            if 'to' in filter_:
                data[f'filters[{i}][1][1]'] = filter_['to']

        return data
