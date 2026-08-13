from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.enums import CategoryType
from integrify.utils import UnsetField


class GetCategoriesRequest(PaginatedDataRequest):
    parent_id: UnsetField[int]
    type: UnsetField[CategoryType]
    include_children: UnsetField[bool]
    include_inactive: UnsetField[bool]


class GetCategoryByIDRequest(ByIDRequest):
    include_children: UnsetField[bool]
