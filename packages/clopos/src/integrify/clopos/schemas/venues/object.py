from integrify.utils import UnsetOrNoneField
from pydantic import BaseModel


class Venue(BaseModel):
    id: int
    """Branch ID"""

    name: str
    """Branch name"""

    address: UnsetOrNoneField[str]
    """Branch address"""

    status: UnsetOrNoneField[int]
    """1 = active, 0 = inactive"""

    phone: UnsetOrNoneField[str]
    """Contact number"""

    email: UnsetOrNoneField[str]
    """Contact email"""

    media: list[str] = []
    """Media URLs"""
