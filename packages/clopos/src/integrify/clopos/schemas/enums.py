from enum import Enum


class CategoryType(str, Enum):
    PRODUCT = 'PRODUCT'
    INGREDIENT = 'INGREDIENT'
    ACCOUNTING = 'ACCOUNTING'


class ProductType(str, Enum):
    GOODS = 'GOODS'
    DISH = 'DISH'
    TIMER = 'TIMER'
    PREPARATION = 'PREPARATION'
    INGREDIENT = 'INGREDIENT'
    MODIFICATION = 'MODIFICATION'


class OrderStatus(str, Enum):
    NEW = 'NEW'
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    READY = 'READY'
    PICKED_UP = 'PICKED_UP'
    CONFIRMED = 'CONFIRMED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    RECEIVED = 'RECEIVED'
    IGNORE = 'IGNORE'


class DiscountType(int, Enum):
    NONE = 0
    PERCENTAGE = 1
    FIXED = 2


class Gender(int, Enum):
    MALE = 1
    FEMALE = 2
