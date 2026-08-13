from decimal import Decimal

from integrify.clopos.schemas.common.object import Balance, CashbackBalance, Timestamp
from integrify.clopos.schemas.enums import DiscountType
from integrify.utils import UnsetOrNoneField


class Group(Timestamp):
    id: int
    """The unique identifier for the customer group"""

    name: str
    """The name of the customer group"""

    discount_type: UnsetOrNoneField[DiscountType]
    """The type of discount applied to the customer group"""

    discount_value: int
    """The discount applied to the customer group"""

    system_type: str
    """The system type of the customer group"""


class Customer(Timestamp):
    id: int
    """The unique identifier for the customer"""

    venue_id: int
    """The ID of the venue the customer belongs to"""

    cid: str
    """The unique identifier for the customer in the POS"""

    group_id: int
    """The ID of the customer group they belong to"""

    group: UnsetOrNoneField[Group]
    """An object containing details of the customer's group"""

    balance_id: int
    """The balance ID of the customer"""

    name: str
    """The name of the customer"""

    discount: UnsetOrNoneField[Decimal]
    """The discount applied to the customer"""

    email: UnsetOrNoneField[str]
    """The email address of the customer"""

    phone: UnsetOrNoneField[str]
    """The primary phone number of the customer"""

    phones: list[str] = []
    """An array of the customer's phone numbers"""

    address: UnsetOrNoneField[str]
    """The address of the customer"""

    addresses: list[str] = []
    """An array of the customer's saved addresses"""

    description: UnsetOrNoneField[str]
    """The description of the customer"""

    address_data: UnsetOrNoneField[list[str]]
    """The customer's address data"""

    bonus_balance_id: UnsetOrNoneField[int]
    """The ID of the customer's bonus balance"""

    balance: UnsetOrNoneField[Balance]
    """Contains details about the customer's store credit balance"""

    cashback_balance_id: UnsetOrNoneField[int]
    """The ID of the customer's cashback balance"""

    cashback_balance: UnsetOrNoneField[CashbackBalance]
    """Contains details about the customer's cashback balance"""

    spent: UnsetOrNoneField[Decimal]
    """The total amount spent by the customer"""

    total_discount: UnsetOrNoneField[Decimal]
    """The total discount applied to the customer"""

    total_bonus: UnsetOrNoneField[Decimal]
    """The total amount of bonus points applied to the customer"""

    receipt_count: UnsetOrNoneField[int]
    """The total number of receipts for the customer"""

    gender: UnsetOrNoneField[int]
    """The gender of the customer"""

    date_of_birth: UnsetOrNoneField[str]
    """The date of birth of the customer"""

    code: UnsetOrNoneField[str]
    """The code of the customer"""

    source: UnsetOrNoneField[str]
    """The source of the customer"""

    reference_id: UnsetOrNoneField[str]
    """The reference ID of the customer"""

    phone_verified_at: UnsetOrNoneField[str]
    """The timestamp when the customer's phone number was verified"""

    status: UnsetOrNoneField[bool]
    """The status of the customer account"""

    can_use_loyalty_system: UnsetOrNoneField[bool]
    """Whether the customer can use the loyalty system or not"""

    is_verified: UnsetOrNoneField[bool]
    """Whether the customer is verified or not"""
