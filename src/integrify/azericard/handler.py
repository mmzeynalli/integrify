from integrify.api import APIPayloadHandler
from integrify.azericard.schemas.request import (
    AuthAndSaveCardRequestSchema,
    AuthConfirmRequestSchema,
    AuthRequestSchema,
    AuthWithSavedCardRequestSchema,
    GetTransactionStatusRequestSchema,
    TransferConfirmDeclineRequestSchema,
    TransferStartRequestSchema,
)
from integrify.azericard.schemas.response import (
    GetTransactionStatusResponseSchema,
    TransferConfirmResponseSchema,
    TransferDeclineResponseSchema,
)

# =============================================================================================== #
# AUTH HANDLERS                                                                                   #
# =============================================================================================== #


class BaseAzericardPayloadHandler(APIPayloadHandler):
    """AzeriCard form-post endpoint-ləri üçün baza handler.

    Bu endpoint-lər üçün `dry=True` (sorğu göndərilmir, HTML form üçün data qaytarılır).
    `req_model` alt class-larda ClassVar kimi təyin olunur.
    """

    dry = True


class AuthPayloadHandler(BaseAzericardPayloadHandler):
    req_model = AuthRequestSchema


class AuthConfirmPayloadHandler(BaseAzericardPayloadHandler):
    req_model = AuthConfirmRequestSchema


class AuthAndSavePayloadHandler(BaseAzericardPayloadHandler):
    req_model = AuthAndSaveCardRequestSchema


class AuthWithSavedCardPayloadHandler(BaseAzericardPayloadHandler):
    req_model = AuthWithSavedCardRequestSchema


class GetTransactionStatusPayloadHandler(APIPayloadHandler):
    req_model = GetTransactionStatusRequestSchema
    resp_model = GetTransactionStatusResponseSchema


# =============================================================================================== #
# TRANSFER HANDLERS                                                                               #
# =============================================================================================== #
class TransferStartPayloadHandler(BaseAzericardPayloadHandler):
    req_model = TransferStartRequestSchema


class TransferConfirmPayloadHandler(APIPayloadHandler):
    req_model = TransferConfirmDeclineRequestSchema
    resp_model = TransferConfirmResponseSchema


class TransferDeclinePayloadHandler(APIPayloadHandler):
    req_model = TransferConfirmDeclineRequestSchema
    resp_model = TransferDeclineResponseSchema  # pragma: no cover
