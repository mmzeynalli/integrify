from decimal import Decimal

from pydantic import BaseModel

from integrify.utils import UnsetOrNoneField


class PriceListPrice(BaseModel):
    id: int
    """Unique identifier of the price entry"""

    list_id: int
    """ID of the price list this price belongs to"""

    product_id: int
    """ID of the product this price applies to"""

    price: Decimal
    """The price value for the product in this list"""

    product: UnsetOrNoneField[dict]
    """The related product object (included with `with[]=product`)"""

    list: UnsetOrNoneField[dict]
    """The related price list object (included with `with[]=list`)"""


class PriceList(BaseModel):
    id: int
    """Unique identifier of the price list"""

    name: str
    """Name of the price list"""

    description: UnsetOrNoneField[str]
    """Description of the price list"""

    status: bool
    """Whether the price list is active"""

    prices: UnsetOrNoneField[list[PriceListPrice]]
    """Prices contained in this list (included with `with[]=prices`)"""

    created_at: UnsetOrNoneField[str]
    """The timestamp when the price list was created"""

    updated_at: UnsetOrNoneField[str]
    """The timestamp when the price list was last updated"""
