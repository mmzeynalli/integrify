from integrify.api import APIPayloadHandler
from integrify.lsim.schemas.request import (
    CheckBalanceRequestSchema,
    GetReportGetRequestSchema,
    SendSMSGetRequestSchema,
    SendSMSPostRequestSchema,
)
from integrify.lsim.schemas.response import BaseResponseSchema


class SendSMSGetPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendSMSGetRequestSchema, BaseResponseSchema)


class SendSMSPostPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendSMSPostRequestSchema, BaseResponseSchema)


class CheckBalancePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(CheckBalanceRequestSchema, BaseResponseSchema)


class GetReportGetPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetReportGetRequestSchema, None)
