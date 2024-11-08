from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CreateOrderResponseSchema(BaseModel):
    id: int
    password: str
    redirect_url: str


# OrderInformationPayloadHandler


class OrderType(BaseModel):
    title: str


class OrderInformationResponseSchema(BaseModel):
    id: int
    type_rid: str = Field(alias='typeRid')
    status: str
    last_status_login: str = Field(alias='lastStatusLogin')
    amount: float
    currency: str
    create_time: str = Field(alias='createTime')
    type: OrderType


# DetailedOrderInformationPayloadHandler


class CardAuthentication(BaseModel):
    needCvv2: bool
    needTds: bool
    tranId: str
    tdsDsTranId: str
    timestamp: datetime
    tdsProtocolVer: str
    eci: str
    tdsARes: str


class CardDetails(BaseModel):
    authentication: CardAuthentication
    expiration: str
    brand: str
    issuerRid: str


class SrcToken(BaseModel):
    id: int
    paymentMethod: str
    role: str
    status: str
    regTime: datetime
    entryMode: str
    displayName: str
    card: CardDetails


class ConsumerDeviceBrowser(BaseModel):
    userAgent: str
    colorDepth: int
    pixelRatio: float
    language: str
    tzOffset: int
    localStorage: bool
    languageReplaced: bool
    resolutionReplaced: bool
    osReplaced: bool
    browserReplaced: bool
    screenW: int
    screenH: int
    screenAvailW: int
    screenAvailH: int
    platform: str
    acceptHeader: str
    ip: str
    refUrl: str
    javaEnabled: bool
    jsEnabled: bool


class ConsumerDevice(BaseModel):
    browser: ConsumerDeviceBrowser


class BusinessAddress(BaseModel):
    country: str
    countryA2: str
    countryN3: int


class Merchant(BaseModel):
    id: int
    rid: str
    title: str
    businessAddress: BusinessAddress
    trustConsumerPhone: bool


class DetailedOrderType(BaseModel):
    allowVoid: bool
    hppTranPhase: str
    secretLength: int
    title: str
    rid: str
    paymentMethods: List[str]
    cardBrands: List[str]
    allowTdsAttempt: bool
    allowTdsCant: bool
    allowTdsChallenged: bool
    allowSurcharge: bool
    allowTranTypes: List[str]
    allowTranPhases: List[str]
    allowAuthKinds: List[str]
    allowCofStoreUsages: List[str]
    orderClass: str
    allowCVV2: bool


class DetailedOrderInformationResponseSchema(BaseModel):
    id: int
    hppUrl: str
    hppRedirectUrl: str
    password: str
    status: str
    prevStatus: Optional[str] = None
    lastStatusLogin: str
    amount: float
    currency: str
    terminal: dict
    srcAmount: float
    srcAmountFull: float
    srcCurrency: str
    dstAmount: Optional[float] = None
    dstCurrency: Optional[str] = None
    createTime: datetime
    finishTime: Optional[datetime] = None
    cvv2AuthStatus: str
    tdsV1AuthStatus: Optional[str] = None
    tdsV2AuthStatus: Optional[str] = None
    tdsServerUrl: Optional[str] = None
    authorizedChargeAmount: float
    clearedChargeAmount: float
    clearedRefundAmount: float
    description: str
    language: str
    srcToken: Optional[SrcToken] = None
    consumerDevice: Optional[ConsumerDevice] = None
    merchant: Merchant
    initiationEnvKind: str
    type: DetailedOrderType
    hppCofCapturePurposes: List[str]
    custAttrs: List[str]
    reportPubs: dict


# RefundOrderPayloadHandler


class Match(BaseModel):
    tranActionId: str
    ridByPmo: str


class RefundOrderResponseSchema(BaseModel):
    approvalCode: str
    match: Match
    pmoResultCode: str
