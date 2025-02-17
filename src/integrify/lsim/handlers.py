from integrify.api import APIPayloadHandler
from integrify.lsim.schemas.request import (
    CheckBalanceRequestSchema,
    GetReportGetRequestSchema,
    GetReportPostRequestSchema,
    SendSMSGetRequestSchema,
    SendSMSPostRequestSchema,
)
from integrify.lsim.schemas.response import (
    BaseResponseSchema,
    ReportGetResponseSchema,
    ReportPostResponseSchema,
)


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
        super().__init__(GetReportGetRequestSchema, ReportGetResponseSchema)

    def handle_response(self, resp):
        data = resp.content.decode()
        resp._content = f'{{"error_code": {data}}}'.encode()  # pylint: disable=protected-access
        return super().handle_response(resp)


class GetReportPostPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetReportPostRequestSchema, ReportPostResponseSchema)
