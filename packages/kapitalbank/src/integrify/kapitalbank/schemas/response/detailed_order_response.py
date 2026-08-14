from datetime import datetime

from integrify.kapitalbank.schemas.enums import TransactionStatus
from integrify.kapitalbank.schemas.utils import BaseSchema
from pydantic import Field


class StoredToken(BaseSchema):
    id: int
    cof_provider_rid: str | None = None
    rid_bycofp: str | None = None


class CardAuthentication(BaseSchema):
    need_cvv2: bool
    need_tds: bool
    tran_id: str | None = None
    tds_ds_tran_id: str | None = None
    timestamp: datetime | None = None
    tds_protocol_ver: str | None = None
    eci: str | None = None
    tds_a_res: str | None = None


class CardDetails(BaseSchema):
    authentication: CardAuthentication | None = None
    expiration: str
    brand: str
    issuer_rid: str | None = None


class SrcToken(BaseSchema):
    id: int
    payment_method: str
    role: str
    status: str
    reg_time: datetime
    entry_mode: str | None = None
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
    payment_methods: list[str]
    card_brands: list[str] | None = None
    allow_tds_attempt: bool
    allow_tds_cant: bool
    allow_tds_challenged: bool
    allow_surcharge: bool
    allow_tran_types: list[str]
    allow_tran_phases: list[str]
    allow_auth_kinds: list[str]
    allow_cof_store_usages: list[str]
    order_class: str
    allow_cvv2: bool = Field(alias='allowCVV2')


class DetailedOrderInformationResponseSchema(BaseSchema):
    id: int
    hpp_url: str
    hpp_redirect_url: str | None = None
    password: str
    status: TransactionStatus
    prev_status: str | None = None
    last_status_login: str
    amount: float
    currency: str
    terminal: dict
    src_amount: float
    src_amount_full: float
    src_currency: str
    dst_amount: float | None = None
    dst_currency: str | None = None
    stored_tokens: list[StoredToken] | None = None
    create_time: datetime
    finish_time: datetime | None = None
    cvv2_auth_status: str
    tds_v1_auth_status: str | None = None
    tds_v2_auth_status: str | None = None
    tds_server_url: str | None = None
    authorized_charge_amount: float
    cleared_charge_amount: float
    cleared_refund_amount: float
    description: str
    language: str
    src_token: SrcToken | None = None
    consumer_device: ConsumerDevice | None = None
    merchant: Merchant
    initiation_env_kind: str
    type: DetailedOrderType
    hpp_cof_capture_purposes: list[str]
    cust_attrs: list[str]
    report_pubs: dict
