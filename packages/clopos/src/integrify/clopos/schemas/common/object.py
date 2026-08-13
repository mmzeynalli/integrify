from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from integrify.clopos.schemas.enums import ProductType
from integrify.utils import UnsetOrNoneField


class Timestamp(BaseModel):
    created_at: str
    """The timestamp when the object was created"""

    updated_at: str
    """The timestamp when the object was last updated"""

    deleted_at: UnsetOrNoneField[str]
    """The timestamp when the object was deleted"""


class Balance(Timestamp):
    id: int
    """Balance ID"""

    system_type: UnsetOrNoneField[str]
    """The system type of the balance"""

    venue_id: UnsetOrNoneField[int]
    """The ID of the venue the balance belongs to"""

    name: UnsetOrNoneField[str]
    """The name of the balance"""

    description: UnsetOrNoneField[str]
    """The description of the balance"""

    type: str
    """Balance type"""

    amount: Decimal
    """The balance amount"""

    position: int
    """The position of the balance"""


class CashbackBalance(BaseModel):
    name: UnsetOrNoneField[str]
    """The name of the balance"""

    type: str
    """Balance type"""

    amount: Decimal
    """The balance amount"""


class Image(BaseModel):
    original: UnsetOrNoneField[str]
    """The original image URL"""

    large: UnsetOrNoneField[str]
    """The large image URL"""

    extra_large: UnsetOrNoneField[str]
    """The extra large image URL"""

    thumb: UnsetOrNoneField[str]
    """The thumbnail image URL"""

    blur_hash: UnsetOrNoneField[str]
    """The blur hash of the image"""


class Media(BaseModel):
    uuid: UnsetOrNoneField[str]
    """The UUID of the media"""

    mime_type: UnsetOrNoneField[str]
    """The MIME type of the media"""

    size: UnsetOrNoneField[int]
    """The size of the media in bytes"""

    urls: Image
    """The image URLs of the media"""

    blur_hash: UnsetOrNoneField[str]
    """The blur hash of the media"""

    dimensions: UnsetOrNoneField[dict]
    """The dimensions of the media"""


class Variant(BaseModel):
    """List of product variants (for GOODS)"""

    id: int
    """Modification ID"""

    parent_id: UnsetOrNoneField[int]
    """The identifier of the parent product"""

    type: Literal[ProductType.MODIFICATION]
    """Modification type"""

    name: str
    """The name of the variant (e.g., "0.5 L")"""

    price: Decimal
    """The sales price of the variant"""

    cost_price: Decimal
    """The cost price of the variant"""

    barcode: UnsetOrNoneField[str]
    """The barcode of the variant"""

    full_name: UnsetOrNoneField[str]
    """The full name of the variant"""

    status: int
    """The status of the variant (1: Active, 0: Inactive)"""


class Modifier(BaseModel):
    id: int
    """The modifier's identifier"""

    name: str
    """The name of the modifier (e.g., "Spicy")"""

    price: Decimal
    """The sales price of the modifier"""

    ingredient: UnsetOrNoneField[dict]
    """If the modifier is linked to an ingredient, contains ingredient information"""


class ModifierGroup(Timestamp):
    """List of modifier groups (for DISH)"""

    id: int
    """The group's identifier"""

    name: str
    """The name of the group (e.g., "Spice Level")"""

    type: int
    """Selection rule (1: Single-choice, 0: Multi-choice)"""

    min_select: int
    """Minimum number of selections"""

    max_select: int
    """Maximum number of selections"""

    modifiers: UnsetOrNoneField[list[Modifier]]
    """The modifiers in the group"""

    adjust_to_portion: bool
    """Whether the group is adjusted to the portion size"""

    status: UnsetOrNoneField[bool]
    """The status of the group"""

    meta: UnsetOrNoneField[dict]
    """The metadata of the group"""

    pivot: UnsetOrNoneField[dict]
    """The pivot information of the group"""


class Package(BaseModel):
    """List of purchasing packages (for INGREDIENT)"""

    id: int
    """The package’s identifier"""

    name: str
    """The name of the package (e.g., “Bundle 10 pcs”)"""

    equal: int
    """The number of base units contained in the package"""


class Tax(BaseModel):
    id: int
    """Tax ID"""

    name: str
    """Tax name"""

    rate: Decimal
    """Tax rate"""


class Price(BaseModel):
    price: Decimal
    """Price"""

    from_: UnsetOrNoneField[int] = Field(alias='from')
    """From which period"""

    venue_id: UnsetOrNoneField[int]
    """The venue ID"""


class TimerSetting(BaseModel):
    interval: int
    """The pricing interval in minutes"""

    prices: list[Price]
    """List of prices by intervals"""


class Service(BaseModel):
    sale_type_id: UnsetOrNoneField[int]
    """The sale type ID"""

    sale_type_name: UnsetOrNoneField[str]
    """The name of the sale type"""

    venue_id: UnsetOrNoneField[int]
    """The venue ID"""

    venue_name: UnsetOrNoneField[str]
    """The name of the venue"""
