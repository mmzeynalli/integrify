from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from integrify.clopos.schemas.common.object import (
    Image,
    Media,
    ModifierGroup,
    Package,
    Price,
    Tax,
    TimerSetting,
    Timestamp,
    Variant,
)
from integrify.clopos.schemas.enums import ProductType
from integrify.clopos.schemas.venues.object import Venue
from integrify.utils import UnsetOrNoneField


class Product(Timestamp):
    id: int
    """Unique identifier"""

    cid: UnsetOrNoneField[str]
    """Unique identifier"""

    parent_id: UnsetOrNoneField[int]
    """Parent product ID, null for root"""

    station_id: UnsetOrNoneField[int]
    """The ID of the station the product belongs to"""

    category_id: UnsetOrNoneField[int]
    """The ID of the category the product belongs to"""

    unit_id: UnsetOrNoneField[int]
    """The ID of the unit the product belongs to"""

    net_output: UnsetOrNoneField[int]
    """Net output of the product"""

    type: UnsetOrNoneField[ProductType]
    """product, ingredient, accounting"""

    name: str
    """The main name of the product"""

    parent_name: UnsetOrNoneField[str]
    """The name of the parent product"""

    image: UnsetOrNoneField[Image]
    """Image of the product"""

    position: UnsetOrNoneField[int]
    """The position of the product in the menu"""

    description: UnsetOrNoneField[str]
    """Description of the product"""

    barcode: UnsetOrNoneField[str]
    """The barcode of the product"""

    gov_code: UnsetOrNoneField[str]
    """The government code of the product"""

    cost: UnsetOrNoneField[Decimal]
    """The cost of the product"""

    status: UnsetOrNoneField[int]
    """1 = active, 0 = inactive"""

    hidden: UnsetOrNoneField[bool]
    """Whether the product is hidden or not"""

    sold_by_weight: UnsetOrNoneField[bool]
    """Whether the product is sold by weight or not"""

    max_age: UnsetOrNoneField[int]
    """The maximum age of the product"""

    discountable: UnsetOrNoneField[bool]
    """Whether the product is discountable or not"""

    giftable: UnsetOrNoneField[bool]
    """Whether the product is giftable or not"""

    has_modifications: UnsetOrNoneField[bool]
    """If true, the product has variants in the modifications array"""

    meta: UnsetOrNoneField[dict]
    """Additional settings and visibility info"""

    setting: UnsetOrNoneField[TimerSetting]
    """Pricing rules for TIMER type products. See Timer Settings"""

    modifications: UnsetOrNoneField[list[Variant]]
    """List of variants for GOODS type products. See Variant Object"""

    modificator_groups: UnsetOrNoneField[list[ModifierGroup]]
    """List of modificator groups for GOODS type products. See Modificator Group Object"""

    recipe: UnsetOrNoneField[list['Product']]
    """Recipe for DISH or PREPARATION type products. See Recipe Item."""

    packages: UnsetOrNoneField[list[Package]]
    """Packages for INGREDIENT type products. See Package Object."""

    variants: list['Product'] = []
    """Variants of the product"""

    e_menu_id: UnsetOrNoneField[int]
    """The ID of the eMenu the product belongs to"""

    emenu_category_id: UnsetOrNoneField[int]
    """The ID of the category the product belongs to in eMenu"""

    emenu_position: UnsetOrNoneField[int]
    """The position of the product in eMenu"""

    emenu_hidden: UnsetOrNoneField[bool]
    """Whether the product is hidden in eMenu or not"""

    accounting_category_id: UnsetOrNoneField[int]
    """The ID of the category the product belongs to in accounting"""

    price: Decimal
    """The base price of the product (variants may have their own prices)"""

    prices: UnsetOrNoneField[list[Price]]
    """The prices of the product"""

    cost_price: UnsetOrNoneField[Decimal]
    """The cost price of the product"""

    markup_rate: UnsetOrNoneField[Decimal]
    """The markup rate of the product"""

    taxes: UnsetOrNoneField[list[Tax]]
    """Taxes applied to the product"""

    cooking_time: UnsetOrNoneField[int]
    """The cooking time of the product"""

    ignore_service_charge: UnsetOrNoneField[bool]
    """Whether the product should ignore the service charge or not"""

    inventory_behavior: UnsetOrNoneField[int]
    """The inventory behavior of the product"""

    low_stock: UnsetOrNoneField[int]
    """Low stock count"""

    unit_weight: UnsetOrNoneField[int]
    """The weight of the product in grams"""

    name_slug: UnsetOrNoneField[str]
    """The slug of the product name"""

    full_name: UnsetOrNoneField[str]
    """The full product name, including variant information"""

    gross_margin: UnsetOrNoneField[Decimal]
    """The gross margin of the product"""

    slug: UnsetOrNoneField[str]
    """The slug of the product"""

    color: UnsetOrNoneField[str]
    """The color of the product"""

    venues: UnsetOrNoneField[list[Venue]]
    """The venues the product is available in"""

    properties: UnsetOrNoneField[Union[dict, list]]
    """The properties of the product"""

    media: UnsetOrNoneField[list[Media]]
    """Media of the product"""

    tags: UnsetOrNoneField[list[dict]]
    """Tags of the product"""

    total_quantity: UnsetOrNoneField[int]
    """The total quantity of the product"""

    total_cost: UnsetOrNoneField[Decimal]
    """The total cost of the product"""

    average_cost: UnsetOrNoneField[Decimal]
    """The average cost of the product"""

    open_receipts_count: UnsetOrNoneField[int]
    """The number of open receipts for the product"""

    created_at: UnsetOrNoneField[str]  # type: ignore[assignment]
    """The timestamp when the object was created"""

    updated_at: UnsetOrNoneField[str]  # type: ignore[assignment]
    """The timestamp when the object was last updated"""


class StopList(BaseModel):
    id: int
    """The ID of the stop list"""

    limit: int
    """The stock limit of the product"""

    timestamp: int
    """Last updated timestamp"""
