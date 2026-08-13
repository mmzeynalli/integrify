from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from integrify.clopos.schemas.common.object import Service, Timestamp
from integrify.clopos.schemas.enums import DiscountType, OrderStatus
from integrify.clopos.schemas.products.object import Product
from integrify.clopos.schemas.sales.object import PaymentMethod, SaleType
from integrify.utils import UnsetField, UnsetOrNoneField


class ServiceIn(BaseModel):
    sale_type_id: int
    sale_type_name: str
    venue_id: int
    venue_name: str


class CustomerIn(BaseModel):
    id: int
    name: str
    customer_discount_type: UnsetField[int] = None
    phone: UnsetField[str] = None
    address: UnsetOrNoneField[str]


class ProductIn(BaseModel):
    product_id: int
    count: int
    product_modificators: UnsetOrNoneField[list[dict]]
    meta: UnsetOrNoneField[dict]


class OrderPayloadIn(BaseModel):
    service: ServiceIn
    customer: CustomerIn
    products: list[ProductIn]
    meta: UnsetOrNoneField[dict]


class OrderProductProduct(BaseModel):
    product: UnsetOrNoneField[Union['Product', list]]
    """The product information"""

    count: int
    """The quantity of the product"""

    status: UnsetOrNoneField[str]
    """The status of the product (e.g., "Active", "Inactive")"""

    product_modificators: UnsetOrNoneField[list[dict]]
    """The modificators of the product"""

    product_hash: UnsetOrNoneField[str]
    """The hash of the product"""


class OrderProductMeta(BaseModel):
    price: UnsetOrNoneField[Decimal]
    """The sales price of the product"""

    order_product: OrderProductProduct
    """The product information"""


class OrderProduct(BaseModel):
    product_id: UnsetOrNoneField[int]
    """The product ID"""

    count: int
    """The quantity of the product"""

    product_modificators: UnsetOrNoneField[list[dict]]
    """The modificators of the product"""

    meta: UnsetOrNoneField[OrderProductMeta]
    """The product information"""


class OrderCustomer(BaseModel):
    id: UnsetOrNoneField[int]
    """The customer ID"""

    name: str
    """The name of the customer"""

    phone: UnsetOrNoneField[str]
    """The phone number of the customer"""

    address: UnsetOrNoneField[str]
    """The address of the customer"""

    customer_discount_type: UnsetOrNoneField[DiscountType]  # noqa: F821
    """The discount type of the customer"""


class OrderPayload(BaseModel):
    service: UnsetOrNoneField[Service]
    """The sale type of the order"""

    customer: UnsetOrNoneField['OrderCustomer']
    """The sale type of the order"""

    products: UnsetOrNoneField[list[OrderProduct]]
    """The products in the order"""

    meta: UnsetOrNoneField[dict]
    """The order information"""

    customer_id: UnsetOrNoneField[int]
    """The customer ID of the order"""

    sale_type_id: UnsetOrNoneField[int]
    """The sale type ID of the order"""

    payload_updated_at: UnsetOrNoneField[str]
    """The timestamp of the last update to the payload"""


class OrderItem(BaseModel):
    id: int
    """The order item's identifier"""

    product_id: int
    """The product ID of the order item"""

    quantity: int
    """The quantity of the order item"""

    unit_price: Decimal
    """The sales price of the order item"""

    total_price: Decimal
    """The total sales price of the order item"""


class Order(Timestamp):
    id: int
    """The unique identifier for the order"""

    venue_id: UnsetOrNoneField[int]
    """The ID of the venue associated with the order"""

    type: UnsetOrNoneField[str]
    """The ID of the sale type associated with the order"""

    integration: UnsetOrNoneField[str]
    """The integration channel associated with the order"""

    integration_uuid: UnsetOrNoneField[str]
    """The UUID of the integration associated with the order"""

    integration_id: UnsetOrNoneField[int]
    """The ID of the integration associated with the order"""

    customer_ref_id: UnsetOrNoneField[str]
    """The reference ID of the customer associated with the order"""

    integration_status: UnsetOrNoneField[str]
    """The status of the integration associated with the order"""

    integration_response: UnsetOrNoneField[str]
    """The response from the integration associated with the order"""

    customer_id: UnsetOrNoneField[int]
    """The ID of the customer associated with the order"""

    receive_user_id: UnsetOrNoneField[int]
    """The ID of the user who received the order"""

    receive_terminal_id: UnsetOrNoneField[int]
    """The ID of the terminal where the order was received"""

    status: OrderStatus
    """Current lifecycle state. accepted orders are sent to the POS"""

    payload: OrderPayload
    """ Payload of the order"""

    receipt_id: UnsetOrNoneField[int]
    """Linked open receipt ID once the POS accepts the order"""

    payment_status: UnsetOrNoneField[str]
    """	Payment state (e.g., pending, paid)"""

    total_amount: UnsetOrNoneField[Decimal]
    """Order grand total"""

    line_items: UnsetOrNoneField[list[OrderItem]]
    """Line items of the order"""

    sale_type: UnsetOrNoneField[SaleType]
    """An object containing details of the associated sale type"""

    payment_method_id: UnsetOrNoneField[int]
    """The ID of the payment method associated with the order"""

    payment_method: UnsetOrNoneField[PaymentMethod]
    """An object containing details of the associated payment method"""

    properties: UnsetOrNoneField[dict]
    """Additional properties of the order"""
