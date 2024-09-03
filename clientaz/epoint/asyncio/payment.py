from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.response import EPointPayWithSavedCardResponseSchema


class EPointPayWithSavedCardRequest(EPointRequest[EPointPayWithSavedCardResponseSchema]): ...
