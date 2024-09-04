from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema


class EPointPaymentRequest(EPointRequest[EPointDecodedCallbackDataSchema]): ...
