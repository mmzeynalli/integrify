from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import EPointRedirectUrlResponseSchema


class EPointGetTransactionStatusRequest(EPointRequest[EPointDecodedCallbackDataSchema]): ...


class EPointSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]): ...
