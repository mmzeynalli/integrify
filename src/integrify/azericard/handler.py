from integrify.api import APIPayloadHandler
from integrify.azericard.schemas.request import (
    AuthConfirmRequestSchema,
    AuthRequestSchema,
    GetTransactionStatusRequestSchema,
    PayAndSaveCardRequestSchema,
    PayWithSavedCardRequestSchema,
)
from integrify.azericard.schemas.response import AuthResponseSchema


class AuthPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(AuthRequestSchema, AuthResponseSchema)


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
        super().__init__(GetTransactionStatusRequestSchema, None)
