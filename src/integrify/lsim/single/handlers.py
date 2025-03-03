from integrify.api import APIPayloadHandler
from integrify.lsim.single.schemas.request import (
    CheckBalanceRequestSchema,
    GetReportGetRequestSchema,
    GetReportPostRequestSchema,
    SendSMSGetRequestSchema,
    SendSMSPostRequestSchema,
)
from integrify.lsim.single.schemas.response import (
    BaseGetResponseSchema,
    BasePostResponseSchema,
    ReportGetResponseSchema,
    ReportPostResponseSchema,
)


class SendSMSGetPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendSMSGetRequestSchema, BaseGetResponseSchema)


class SendSMSPostPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendSMSPostRequestSchema, BasePostResponseSchema)


class CheckBalancePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(CheckBalanceRequestSchema, BaseGetResponseSchema)


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
