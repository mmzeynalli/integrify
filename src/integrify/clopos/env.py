import os
from enum import Enum

from integrify.utils import Environment

VERSION = '2.0.0'  # Clopos Open API version targeted by this client

# ENV VARS HERE
CLOPOS_CLIENT_ID: str = os.getenv('CLOPOS_CLIENT_ID', '')
CLOPOS_CLIENT_SECRET: str = os.getenv('CLOPOS_CLIENT_SECRET', '')
CLOPOS_BRAND: str = os.getenv('CLOPOS_BRAND', '')
CLOPOS_INTEGRATOR_ID: str = os.getenv('CLOPOS_INTEGRATOR_ID', '')
# v2-də auth JWT-si brand/venue/integrator-i encode edir. `x-venue` opsional olaraq
# JWT-dəki venue-nu konkret sorğu üçün override etmək üçün saxlanılır.
CLOPOS_VENUE_ID: str = os.getenv('CLOPOS_VENUE_ID', '')
CLOPOS_ENV: str = os.getenv('CLOPOS_ENV', Environment.TEST.value)


class API(str, Enum):
    """Endpoint constant-ları (Clopos Open API v2)"""

    BASE_URL = 'https://integrations.clopos.com/open-api/v2/'

    AUTH = 'auth'

    VENUES = 'venues'

    USERS = 'users'
    USER_BY_ID = 'users/{id}'

    CUSTOMERS = 'customers'
    CUSTOMER_BY_ID = 'customers/{id}'
    CUSTOMER_GROUPS = 'customer-groups'

    CATEGORIES = 'categories'
    CATEGORY_BY_ID = 'categories/{id}'

    STATIONS = 'stations'
    STATION_BY_ID = 'stations/{id}'

    PRODUCTS = 'products'
    PRODUCT_BY_ID = 'products/{id}'
    STOP_LIST = 'products/stop-list'

    SALE_TYPES = 'sale-types'
    PAYMENT_METHODS = 'payment-methods'

    ORDERS = 'orders'
    ORDER_BY_ID = 'orders/{id}'

    RECEIPTS = 'receipts'
    RECEIPT_BY_ID = 'receipts/{id}'
    RECEIPT_CLOSE = 'receipts/{id}/close'
    RECEIPT_STOCK_OPERATIONS = 'receipts/{id}/stock-operations'

    PRICE_LISTS = 'price-lists'
    PRICE_LIST_PRICES = 'price-lists/prices'


__all__ = [
    'VERSION',
    'CLOPOS_CLIENT_ID',
    'CLOPOS_CLIENT_SECRET',
    'CLOPOS_ENV',
    'API',
]
