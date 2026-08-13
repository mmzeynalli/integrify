from integrify.clopos.schemas.common.request import PaginatedDataRequest
from integrify.utils import UnsetField


class GetStationsRequest(PaginatedDataRequest):
    status: UnsetField[int]
    can_print: UnsetField[bool]
