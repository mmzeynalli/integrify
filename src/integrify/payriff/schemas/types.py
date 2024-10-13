from pydantic import BaseModel

from integrify.payriff.schemas.parts import ResultCodes


class PayriffMinimalResponse(BaseModel):
    code: ResultCodes
    internalMessage: str
    route: str
    message: str
    # message: ResultMessages
