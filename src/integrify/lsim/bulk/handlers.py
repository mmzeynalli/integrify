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


class HeadOnlyPayloadHandler(APIPayloadHandler):
    def post_handle_payload(self, data: dict):
        return {'request': {'head': data}}


class SendBulkSMSOneMessagePayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendBulkSMSOneMessageRequestSchema, SendBulkSMSResponseSchema)

    def post_handle_payload(self, data: dict):
        msisdns = data.pop('msisdns')

        return {'request': {'head': data, 'body': [{'msisdn': msisdn} for msisdn in msisdns]}}


class SendBulkSMSDifferentMessagesPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(SendBulkSMSDifferentMessagesRequestSchema, SendBulkSMSResponseSchema)

    def post_handle_payload(self, data: dict):
        msisdns = data.pop('msisdns')
        messages = data.pop('messages')

        return {
            'request': {
                'head': data,
                'body': [
                    {'msisdn': msisdn, 'message': message}
                    for msisdn, message in zip(msisdns, messages)
                ],
            }
        }


class GetBulkSMSReportPayloadHandler(HeadOnlyPayloadHandler):
    def __init__(self):
        super().__init__(GetBulkSMSReportRequestSchema, GetBulkSMSReportResponseSchema)


class GetBulkSMSDeatiledReportPayloadHandler(HeadOnlyPayloadHandler):
    def __init__(self):
        super().__init__(
            GetBulkSMSDeatiledReportRequestSchema,
            GetBulkSMSDetailedReportResponseSchema,
        )


class GetBulkSMSDeatiledWithDateReportPayloadHandler(HeadOnlyPayloadHandler):
    def __init__(self):
        super().__init__(
            GetBulkSMSDeatiledWithDateReportRequestSchema,
            GetBulkSMSDetailedReportResponseSchema,
        )


class GetBalancePayloadHandler(HeadOnlyPayloadHandler):
    def __init__(self):
        super().__init__(GetBalanceRequestSchema, GetBalanceResponseSchema)
