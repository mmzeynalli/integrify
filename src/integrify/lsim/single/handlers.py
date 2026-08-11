import json

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
    req_model = SendSMSGetRequestSchema
    resp_model = BaseGetResponseSchema


class SendSMSPostPayloadHandler(APIPayloadHandler):
    req_model = SendSMSPostRequestSchema
    resp_model = BasePostResponseSchema


class CheckBalancePayloadHandler(APIPayloadHandler):
    req_model = CheckBalanceRequestSchema
    resp_model = BaseGetResponseSchema


class GetReportGetPayloadHandler(APIPayloadHandler):
    req_model = GetReportGetRequestSchema
    resp_model = ReportGetResponseSchema

    def handle_response(self, resp):
        # LSIM report GET endpoint-i body kimi tək bir kod (integer) qaytarır.
        # Onu düzgün JSON-a çeviririk. Əvvəlki versiya `f'{{"error_code": {data}}}'`
        # istifadə edirdi — body integer deyilsə (boş/mətn) yararsız JSON yaradıb crash edirdi.
        raw = resp.content.decode(errors='replace').strip()

        try:
            error_code = int(raw)
        except (TypeError, ValueError):
            error_code = None

        resp._content = json.dumps({'error_code': error_code}).encode()  # pylint: disable=protected-access
        return super().handle_response(resp)


class GetReportPostPayloadHandler(APIPayloadHandler):
    req_model = GetReportPostRequestSchema
    resp_model = ReportPostResponseSchema
