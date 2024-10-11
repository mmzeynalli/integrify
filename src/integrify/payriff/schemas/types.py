from pydantic import BaseModel

from integrify.payriff.schemas.parts import ResultCodes, ResultMessages


class PayriffMinimalResponse(BaseModel):
    code: ResultCodes
    internalMessage: str
    message: ResultMessages
