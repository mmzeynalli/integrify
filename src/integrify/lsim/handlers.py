from integrify.api import APIPayloadHandler
from integrify.lsim.schemas.request import (
    CheckBalanceRequestSchema,
    GetReportRequestSchema,
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


class GetReportPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetReportRequestSchema, BaseResponseSchema)
