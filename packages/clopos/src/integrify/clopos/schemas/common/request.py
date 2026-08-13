from integrify.schemas import PayloadBaseModel
from integrify.utils import UnsetField


class ByIDRequest(PayloadBaseModel):
    URL_PARAM_FIELDS = {'id'}
    id: int


class PaginatedDataRequest(PayloadBaseModel):
    page: UnsetField[int]
    limit: UnsetField[int]
