from typing import Union

from integrify.clopos.schemas.common.object import Timestamp
from integrify.utils import UnsetOrNoneField


class User(Timestamp):
    id: int
    """Unique user identifier"""

    email: UnsetOrNoneField[str]
    """Email address associated with the user"""

    username: str
    """Display name shown in the POS"""

    first_name: UnsetOrNoneField[str]
    """First name of the user"""

    last_name: UnsetOrNoneField[str]
    """last name of the user"""

    pin: str
    """POS PIN code"""

    card: UnsetOrNoneField[str]
    """POS card number"""

    mobile_number: UnsetOrNoneField[str]
    """Mobile number of the user"""

    owner: int
    """1 if the user owns the brand, otherwise 0"""

    hide: int
    """1 if hidden from POS selection, otherwise 0"""

    salary: UnsetOrNoneField[int]
    """Salary of the user"""

    barcode: UnsetOrNoneField[str]
    """POS barcode number"""

    tip_message: UnsetOrNoneField[str]
    """Tip message shown in the POS"""

    can_receive_tips: UnsetOrNoneField[bool]
    """Whether the user can receive tips or not"""

    login_at: UnsetOrNoneField[str]
    """Timestamp when the user logged in"""

    status: bool
    """Indicates whether the user account is active"""

    bonus_balance_id: UnsetOrNoneField[int]
    """Balance ID of the user"""

    properties: UnsetOrNoneField[Union[dict, list]]
    """User properties"""

    image: UnsetOrNoneField[list[str]]
    """User images"""
