from integrify.api import APIPayloadHandler
from integrify.azericard.schemas.request import (
    AuthConfirmRequestSchema,
    AuthRequestSchema,
    ConfirmTransferRequestSchema,
    GetTransactionStatusRequestSchema,
    PayAndSaveCardRequestSchema,
    PayWithSavedCardRequestSchema,
    StartTransferRequestSchema,
)
from integrify.azericard.schemas.response import GetTransactionStatusResponseSchema


class AuthPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(AuthRequestSchema, None)


class AuthConfirmPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(AuthConfirmRequestSchema, None)


class PayAndSavePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(PayAndSaveCardRequestSchema, None)


class PayWithSavedCardPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(PayWithSavedCardRequestSchema, None)


class GetTransactionStatusPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetTransactionStatusRequestSchema, GetTransactionStatusResponseSchema)


class StartTransferPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(StartTransferRequestSchema, None)


class ConfirmTransactionPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(ConfirmTransferRequestSchema, None)
