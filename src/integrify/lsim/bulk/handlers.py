from integrify.api import APIPayloadHandler
from integrify.lsim.bulk.schemas.request import (
    GetBalanceRequestSchema,
    GetBulkSMSDeatiledReportRequestSchema,
    GetBulkSMSDeatiledWithDateReportRequestSchema,
    GetBulkSMSReportRequestSchema,
    SendBulkSMSDifferentMessagesRequestSchema,
    SendBulkSMSOneMessageRequestSchema,
)
from integrify.lsim.bulk.schemas.response import (
    GetBalanceResponseSchema,
    GetBulkSMSDetailedReportResponseSchema,
    GetBulkSMSReportResponseSchema,
    SendBulkSMSResponseSchema,
)


class SendBulkSMSOneMessagePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendBulkSMSOneMessageRequestSchema, SendBulkSMSResponseSchema)


class SendBulkSMSDifferentMessagesPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendBulkSMSDifferentMessagesRequestSchema, SendBulkSMSResponseSchema)


class GetBulkSMSReportPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetBulkSMSReportRequestSchema, GetBulkSMSReportResponseSchema)


class GetBulkSMSDeatiledReportPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(
            GetBulkSMSDeatiledReportRequestSchema,
            GetBulkSMSDetailedReportResponseSchema,
        )


class GetBulkSMSDeatiledWithDateReportPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(
            GetBulkSMSDeatiledWithDateReportRequestSchema,
            GetBulkSMSDetailedReportResponseSchema,
        )


class GetBalancePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(GetBalanceRequestSchema, GetBalanceResponseSchema)
