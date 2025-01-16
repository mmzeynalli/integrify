from datetime import datetime
from typing import Dict, List, Optional

from pydantic import Field

from integrify.kapital.schemas.enums import TransactionStatus
from integrify.kapital.schemas.utils import BaseSchema


class StoredToken(BaseSchema):
    id: int
    cof_provider_rid: Optional[str] = None
    rid_bycofp: Optional[str] = None


class CardAuthentication(BaseSchema):
    need_cvv2: bool
    need_tds: bool
    tran_id: Optional[str] = None
    tds_ds_tran_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    tds_protocol_ver: Optional[str] = None
    eci: Optional[str] = None
    tds_a_res: Optional[str] = None


class CardDetails(BaseSchema):
    authentication: Optional[CardAuthentication] = None
    expiration: str
    brand: str
    issuer_rid: Optional[str] = None


class SrcToken(BaseSchema):
    id: int
    payment_method: str
    role: str
    status: str
    reg_time: datetime
    entry_mode: Optional[str] = None
    display_name: str
    card: CardDetails


class ConsumerDeviceBrowser(BaseSchema):
    user_agent: str
    color_depth: int
    pixel_ratio: float
    language: str
    tz_offset: int
    local_storage: bool
    language_replaced: bool
    resolution_replaced: bool
    os_replaced: bool
    browser_replaced: bool
    screen_w: int
    screen_h: int
    screen_avail_w: int
    screen_avail_h: int
    platform: str
    accept_header: str
    ip: str
    ref_url: str
    java_enabled: bool
    js_enabled: bool


class ConsumerDevice(BaseSchema):
    browser: ConsumerDeviceBrowser


class BusinessAddress(BaseSchema):
    country: str
    country_a2: str
    country_n3: int


class Merchant(BaseSchema):
    id: int
    rid: str
    title: str
    business_address: BusinessAddress
    trust_consumer_phone: bool


class DetailedOrderType(BaseSchema):
    allow_void: bool
    hpp_tran_phase: str
    secret_length: int
    title: str
    rid: str
    payment_methods: List[str]
    card_brands: Optional[List[str]] = None
    allow_tds_attempt: bool
    allow_tds_cant: bool
    allow_tds_challenged: bool
    allow_surcharge: bool
    allow_tran_types: List[str]
    allow_tran_phases: List[str]
    allow_auth_kinds: List[str]
    allow_cof_store_usages: List[str]
    order_class: str
    allow_cvv2: bool = Field(alias='allowCVV2')


class DetailedOrderInformationResponseSchema(BaseSchema):
    id: int
    hpp_url: str
    hpp_redirect_url: Optional[str] = None
    password: str
    status: TransactionStatus
    prev_status: Optional[str] = None
    last_status_login: str
    amount: float
    currency: str
    terminal: Dict
    src_amount: float
    src_amount_full: float
    src_currency: str
    dst_amount: Optional[float] = None
    dst_currency: Optional[str] = None
    stored_tokens: Optional[List[StoredToken]] = None
    create_time: datetime
    finish_time: Optional[datetime] = None
    cvv2_auth_status: str
    tds_v1_auth_status: Optional[str] = None
    tds_v2_auth_status: Optional[str] = None
    tds_server_url: Optional[str] = None
    authorized_charge_amount: float
    cleared_charge_amount: float
    cleared_refund_amount: float
    description: str
    language: str
    src_token: Optional[SrcToken] = None
    consumer_device: Optional[ConsumerDevice] = None
    merchant: Merchant
    initiation_env_kind: str
    type: DetailedOrderType
    hpp_cof_capture_purposes: List[str]
    cust_attrs: List[str]
    report_pubs: Dict
