from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import (
    EPointMinimalResponseSchema,
    EPointPayoutResponseSchema,
    EPointPayWithSavedCardResponseSchema,
    EPointRedirectUrlResponseSchema,
)


class EPointPaymentRequest(EPointRequest[EPointDecodedCallbackDataSchema]): ...


class EPointPayWithSavedCardRequest(EPointRequest[EPointPayWithSavedCardResponseSchema]): ...


class EPointPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]): ...


class EPointPayoutRequest(EPointRequest[EPointPayoutResponseSchema]): ...


class EPointRefundRequest(EPointRequest[EPointMinimalResponseSchema]): ...
