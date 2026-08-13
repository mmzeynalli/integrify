from typing import Union

from pydantic import Field

from integrify.clopos.schemas.common.object import Image, Media, Timestamp
from integrify.clopos.schemas.enums import CategoryType
from integrify.utils import UnsetOrNoneField


class Category(Timestamp):
    id: int
    """Unique identifier"""

    name: str
    """Name of the category"""

    status: int
    """1 = active, 0 = inactive"""

    hidden: bool
    """Whether the category is hidden or not"""

    type: CategoryType
    """product_category, ingredient_category, accounting_category"""

    image: UnsetOrNoneField[Image]
    """Image of the category"""

    position: UnsetOrNoneField[int]
    """The position of the category"""

    emenu_position: UnsetOrNoneField[int]
    """The position of the category in the eMenu"""

    meta: UnsetOrNoneField[dict]
    """Additional settings and visibility info"""

    emenu_hidden: UnsetOrNoneField[bool]
    """Whether the category is hidden in the eMenu or not"""

    code: UnsetOrNoneField[str]
    """The code of the category"""

    lft: int = Field(alias='_lft')
    """Nested set boundaries"""

    rgt: int = Field(alias='_rgt')
    """Nested set boundaries"""

    depth: int
    """Depth of the subcategory"""

    parent_id: UnsetOrNoneField[int]
    """Parent category ID, null for root"""

    slug: UnsetOrNoneField[str]
    """URL-friendly identifier"""

    color: UnsetOrNoneField[str]
    """HEX color"""

    properties: UnsetOrNoneField[Union[dict, list]]
    """Additional settings and visibility info"""

    media: list[Media]
    """Media of the category"""

    children: UnsetOrNoneField[list['Category']]
    """Subcategories"""
