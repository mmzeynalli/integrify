from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import EPointRedirectResponseSchema
from clientaz.epoint.sync.base import EPointRequest


class EPointGetTransactionStatusRequest(EPointRequest[EPointDecodedCallbackDataSchema]):
    def __init__(self, transaction_id: str):
        super().__init__()
        self.verb = 'POST'
        self.path = '/api/1/get-status'
        self.data['transaction'] = transaction_id


class EPointSaveCardRequest(EPointRequest[EPointRedirectResponseSchema]):
    def __init__(self):
        super().__init__()
        self.path = '/api/1/card-registration'
        self.verb = 'POST'
