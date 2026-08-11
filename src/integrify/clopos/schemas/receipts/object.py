from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from integrify.clopos.helpers import IsoDateTime
from integrify.clopos.schemas.common.object import Timestamp
from integrify.clopos.schemas.enums import DiscountType, OrderStatus
from integrify.utils import UnsetField, UnsetOrNoneField


class ReceiptProductIn(BaseModel):
    model_config = {'extra': 'allow'}

    id: UnsetField[int]
    """The unique identifier for the receipt product"""

    cid: str
    """The CID of the receipt product"""

    product_id: int
    """The ID of the product associated with the receipt product"""

    meta: dict
    """The meta data of the receipt product"""

    count: int
    """The count of the receipt product"""

    portion_size: Decimal
    """The portion size of the receipt product"""

    total: Decimal
    """The total of the receipt product"""

    price: Decimal
    """The price of the receipt product"""

    cost: UnsetField[Decimal]
    """The cost of the receipt product"""

    is_gift: bool
    """Whether the receipt product is a gift"""

    created_at: UnsetField[IsoDateTime]
    """The created at of the receipt product"""

    updated_at: UnsetField[IsoDateTime]
    """The updated at of the receipt product"""

    terminal_updated_at: UnsetField[IsoDateTime]
    """The terminal updated at of the receipt product"""

    deleted_at: UnsetField[IsoDateTime]
    """The deleted at of the receipt product"""


class ReceiptPaymentMethod(BaseModel):
    id: int
    """The payment method ID"""

    name: str
    """The name of the payment method"""

    amount: Decimal
    """The amount of the payment method"""


class ReceiptProduct(ReceiptProductIn):
    receipt_id: int
    """The ID of the receipt associated with the receipt product"""

    product_hash: Optional[str]
    """The hash of the product associated with the receipt product"""

    preprint_count: int
    """The preprint count of the receipt product"""

    station_printed_count: int
    """The station printed count of the receipt product"""

    station_aborted_count: int
    """The station aborted count of the receipt product"""

    seller_id: int
    """The ID of the seller associated with the receipt product"""

    loyalty_type: Optional[str]
    """The loyalty type of the receipt product"""

    loyalty_value: Optional[Decimal]
    """The loyalty value of the receipt product"""

    discount_rate: Decimal
    """The discount rate of the receipt product"""

    discount_value: Decimal
    """The discount value of the receipt product"""

    discount_type: Optional[DiscountType]
    """The discount type of the receipt product"""

    total_discount: Decimal
    """The total discount of the receipt product"""

    subtotal: Decimal
    """The subtotal of the receipt product"""

    receipt_discount: Decimal
    """The receipt discount of the receipt product"""

    receipt_product_modificators: list
    """The receipt product modificators of the receipt product"""

    taxes: list
    """The taxes of the receipt product"""


class Receipt(Timestamp):
    id: int
    """Unique receipt identifier"""

    venue_id: UnsetOrNoneField[int]
    """The ID of the venue associated with the receipt"""

    cash_shift_cid: UnsetOrNoneField[str]
    """The UUID of the cash shift associated with the receipt"""

    cid: UnsetOrNoneField[str]
    """Transaction UUID"""

    user_id: UnsetOrNoneField[int]
    """The ID of the user associated with the receipt"""

    open_by_user_id: UnsetOrNoneField[int]
    """The ID of the user who opened the receipt"""

    close_by_user_id: UnsetOrNoneField[int]
    """The ID of the user who closed the receipt"""

    courier_id: UnsetOrNoneField[int]
    """The ID of the courier associated with the receipt"""

    seller_id: UnsetOrNoneField[int]
    """The ID of the seller associated with the receipt"""

    terminal_id: UnsetOrNoneField[int]
    """The ID of the terminal associated with the receipt"""

    source: UnsetOrNoneField[str]
    """The source of the receipt"""

    closed_terminal_id: UnsetOrNoneField[int]
    """The ID of the terminal where the receipt was closed"""

    service_notification_id: UnsetOrNoneField[int]
    """The ID of the service notification associated with the receipt"""

    table_id: UnsetOrNoneField[int]
    """The ID of the table associated with the receipt"""

    hall_id: UnsetOrNoneField[int]
    """The ID of the hall associated with the receipt"""

    customer_id: UnsetOrNoneField[int]
    """The ID of the customer associated with the receipt"""

    sale_type_id: UnsetOrNoneField[int]
    """Sale type identifier"""

    is_returns: UnsetOrNoneField[bool]
    """Whether the receipt is a return"""

    guests: UnsetOrNoneField[int]
    """The number of guests associated with the receipt"""

    status: UnsetOrNoneField[int]
    """Receipt status code"""

    local_status: UnsetOrNoneField[int] = None
    """Receipt local status"""

    lock: UnsetOrNoneField[bool]
    """Lock identifier"""

    inventory_status: UnsetOrNoneField[int]
    """Inventory status code"""

    report_status: UnsetOrNoneField[int]
    """Report status code"""

    meta: UnsetOrNoneField[dict]
    """Receipt meta data"""

    suspicion: UnsetOrNoneField[int]
    """Suspicion level code"""

    printed: UnsetOrNoneField[bool]
    """Whether the receipt has been printed"""

    total: UnsetOrNoneField[Decimal]
    """Total amount collected"""

    subtotal: UnsetOrNoneField[Decimal]
    """Subtotal before adjustments"""

    original_subtotal: UnsetOrNoneField[Decimal]
    """Receipt original subtotal"""

    gift_total: UnsetOrNoneField[Decimal]
    """Receipt gift total"""

    total_cost: UnsetOrNoneField[Decimal] = Field(alias='totalCost')
    """Receipt total cost"""

    payment_methods: UnsetOrNoneField[list[ReceiptPaymentMethod]]
    """Payment methods associated with the receipt"""

    fiscal_id: UnsetOrNoneField[str]
    """Receipt fiscal ID"""

    by_cash: UnsetOrNoneField[Decimal]
    """Amount collected by cash"""

    by_card: UnsetOrNoneField[Decimal]
    """Amount collected by card"""

    remaining: UnsetOrNoneField[Decimal]
    """Remaining amount"""

    customer_discount_type: UnsetOrNoneField[int] = None
    """Customer discount type"""

    discount_type: UnsetOrNoneField[DiscountType]
    """Discount type"""

    discount_value: UnsetOrNoneField[Decimal]
    """Discount value"""

    discount_rate: UnsetOrNoneField[Decimal]
    """Discount rate"""

    rps_discount: UnsetOrNoneField[Decimal]
    """RPS discount"""

    service_charge: UnsetOrNoneField[Decimal]
    """Service charge"""

    service_charge_value: UnsetOrNoneField[Decimal]
    """Service charge value"""

    i_tax: UnsetOrNoneField[Decimal]
    """I tax"""

    delivery_fee: UnsetOrNoneField[Decimal]
    """Delivery fee"""

    e_tax: UnsetOrNoneField[Decimal]
    """E tax"""

    total_tax: UnsetOrNoneField[Decimal]
    """Total tax"""

    description: UnsetOrNoneField[str]
    """Receipt description"""

    address: UnsetOrNoneField[str]
    """Receipt address"""

    terminal_version: UnsetOrNoneField[str]
    """Receipt terminal version"""

    loyalty_type: UnsetOrNoneField[int]
    """Loyalty type"""

    loyalty_value: UnsetOrNoneField[Decimal]
    """Loyalty value"""

    order_status: UnsetOrNoneField[OrderStatus]
    """Order status code"""

    order_number: UnsetOrNoneField[str]
    """Order number"""

    receipt_products: UnsetOrNoneField[list[ReceiptProduct]] = None
    """Receipt products"""

    terminal_updated_at: UnsetOrNoneField[str]
    """Receipt terminal updated at"""

    closed_at: UnsetOrNoneField[str]
    """Receipt closed at"""

    shift_date: UnsetOrNoneField[str]
    """Shift date associated with the receipt"""

    gift_count: UnsetOrNoneField[int]
    """Receipt gift count"""

    total_discount: UnsetOrNoneField[Decimal]
    """Receipt total discount"""

    properties: UnsetOrNoneField[dict]
    """Receipt properties"""


class ReceiptStockOperation(BaseModel):
    id: int
    """Unique identifier of the stock operation"""

    receipt_id: int
    """ID of the receipt that generated this operation"""

    receipt_product_id: UnsetOrNoneField[int]
    """ID of the receipt product, if applicable"""

    product_id: int
    """ID of the product whose stock changed"""

    stock_id: int
    """ID of the stock record"""

    storage_id: int
    """ID of the storage the stock belongs to"""

    quantity: Decimal
    """The quantity deducted (or added) by this operation"""

    before_quantity: Decimal
    """Stock quantity before the operation"""

    after_quantity: Decimal
    """Stock quantity after the operation"""

    cost: Decimal
    """Unit cost used for the operation"""

    before_cost: Decimal
    """Cost before the operation"""

    total_cost: Decimal
    """Total cost of the operation"""

    operated_at: UnsetOrNoneField[str]
    """Timestamp of the operation (YYYY-MM-DD HH:mm:ss)"""

    product: UnsetOrNoneField[dict]
    """The related product object"""

    stock: UnsetOrNoneField[dict]
    """The related stock object"""
