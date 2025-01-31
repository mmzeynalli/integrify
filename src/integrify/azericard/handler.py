from typing import Optional, Union

from integrify.api import APIPayloadHandler
from integrify.azericard.schemas.request import (
    AuthAndSaveCardRequestSchema,
    AuthConfirmRequestSchema,
    AuthRequestSchema,
    AuthWithSavedCardRequestSchema,
    ConfirmTransferRequestSchema,
    GetTransactionStatusRequestSchema,
    StartTransferRequestSchema,
)
from integrify.azericard.schemas.response import GetTransactionStatusResponseSchema
from integrify.schemas import PayloadBaseModel, _ResponseT


class BaseAzericardPayloadHandler(APIPayloadHandler):
    def __init__(
        self,
        req_model: Optional[type[PayloadBaseModel]] = None,
        resp_model: Union[type[_ResponseT], type[dict], None] = dict,
        dry: bool = True,
    ):
        super().__init__(req_model, resp_model, dry)


class AuthPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=AuthRequestSchema)


class AuthConfirmPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=AuthConfirmRequestSchema)


class AuthAndSavePayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=AuthAndSaveCardRequestSchema)


class AuthWithSavedCardPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=AuthWithSavedCardRequestSchema)


class GetTransactionStatusPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(
            GetTransactionStatusRequestSchema,
            GetTransactionStatusResponseSchema,
            dry=False,
        )


class StartTransferPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=StartTransferRequestSchema)


class ConfirmTransactionPayloadHandler(BaseAzericardPayloadHandler):
    def __init__(self):
        super().__init__(req_model=ConfirmTransferRequestSchema)
