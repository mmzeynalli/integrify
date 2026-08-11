# pylint: disable=wrong-import-order,ungrouped-imports
import json
from functools import cached_property
from typing import Annotated, Union

from pydantic import Field

from integrify.api import APIPayloadHandler
from integrify.clopos import env
from integrify.clopos.schemas.auth.request import AuthRequest
from integrify.clopos.schemas.auth.response import AuthResponse
from integrify.clopos.schemas.categories.object import Category
from integrify.clopos.schemas.categories.request import GetCategoriesRequest, GetCategoryByIDRequest
from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.common.response import (
    ErrorResponse,
    ObjectListResponse,
    ObjectResponse,
)
from integrify.clopos.schemas.customers.object import Customer
from integrify.clopos.schemas.customers.request import CreateCustomerRequest, GetCustomersRequest
from integrify.clopos.schemas.orders.object import Order
from integrify.clopos.schemas.orders.request import (
    CreateOrderRequest,
    GetOrderByIDRequest,
    GetOrdersRequest,
    UpdateOrderRequest,
)
from integrify.clopos.schemas.products.object import Product, StopList
from integrify.clopos.schemas.products.request import (
    GetProductByIDRequest,
    GetProductsRequest,
    GetStopListRequest,
)
from integrify.clopos.schemas.receipts.object import Receipt, ReceiptStockOperation
from integrify.clopos.schemas.receipts.request import (
    CloseReceiptRequest,
    GetReceiptsRequest,
    UpdateClosedReceiptRequest,
)
from integrify.clopos.schemas.stations.object import Station
from integrify.clopos.schemas.stations.request import GetStationsRequest


class AuthHandler(APIPayloadHandler):
    def __init__(
        self,
        req_model=AuthRequest,
        resp_model=Annotated[Union[AuthResponse, ErrorResponse], Field(discriminator='success')],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)  # ty: ignore[invalid-argument-type]


class AuthedAPIPayloadHandler(APIPayloadHandler):
    def __init__(self, req_model=None, resp_model=None, dry=False):
        super().__init__(
            req_model,
            Annotated[
                Union[resp_model, ErrorResponse], Field(discriminator='success')
            ],  # ty: ignore[invalid-argument-type]
            dry,
        )

    @cached_property
    def headers(self):
        default = super().headers

        # v2: yalnız `x-token` tələb olunur (JWT brand/venue/integrator-i encode edir).
        # `x-venue` opsional olaraq JWT-dəki venue-nu konkret sorğu üçün override edir.
        if env.CLOPOS_VENUE_ID:
            default['x-venue'] = env.CLOPOS_VENUE_ID

        return default


def GetPaginatedDataHandler(object_type, req_model=PaginatedDataRequest):  # pylint: disable=invalid-name
    """Function to dynamically create ObjectListResponse[object_type]"""

    class _GetPaginatedDataHandler(AuthedAPIPayloadHandler):
        def __init__(self, dry=False):
            super().__init__(
                req_model=req_model,
                resp_model=ObjectListResponse[object_type],
                dry=dry,
            )

    return _GetPaginatedDataHandler


def GetByIDHandler(object_type, req_model=ByIDRequest):  # pylint: disable=invalid-name
    """Function to dynamically create ObjectResponse[object_type]"""

    class _GetByIDHandler(AuthedAPIPayloadHandler):
        def __init__(self, dry=False):
            super().__init__(
                req_model=req_model,
                resp_model=ObjectResponse[object_type],
                dry=dry,
            )

    return _GetByIDHandler


###################################################################################################


class GetCustomersHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetCustomersRequest,
        resp_model=ObjectListResponse[Customer],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class CreateCustomerHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=CreateCustomerRequest,
        resp_model=ObjectResponse[Customer],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetCategoriesHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetCategoriesRequest,
        resp_model=ObjectListResponse[Category],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetCategoryByIDHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetCategoryByIDRequest,
        resp_model=ObjectResponse[Category],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetStationsHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetStationsRequest,
        resp_model=ObjectListResponse[Station],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetProductsHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetProductsRequest,
        resp_model=ObjectListResponse[Product],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)

    def post_handle_payload(self, data):
        return json.dumps(data)  # for urlencoding


class GetProductByIDHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetProductByIDRequest,
        resp_model=ObjectResponse[Product],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetStopListHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetStopListRequest,
        resp_model=ObjectListResponse[StopList],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetOrdersHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetOrdersRequest,
        resp_model=ObjectListResponse[Order],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetOrderByIDHandler(AuthedAPIPayloadHandler):
    def __init__(self, req_model=GetOrderByIDRequest, resp_model=ObjectResponse[Order], dry=False):
        super().__init__(req_model, resp_model, dry)


class CreateOrderHandler(AuthedAPIPayloadHandler):
    def __init__(self, req_model=CreateOrderRequest, resp_model=ObjectResponse[Order], dry=False):
        super().__init__(req_model, resp_model, dry)


class UpdateOrderHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=UpdateOrderRequest,
        resp_model=ObjectResponse[Order],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetReceiptsHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=GetReceiptsRequest,
        resp_model=ObjectListResponse[Receipt],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class _UpdateReceiptHandler(AuthedAPIPayloadHandler):
    def handle_payload(self, req_model, *args, **kwds):
        # Fərqli olaraq base handler-dən, burada `URL_PARAM_FIELDS` body-dən çıxarılmır
        # (yəni id həm URL-də, həm body-də göndərilir).
        if self.req_model and req_model is not None:
            return req_model.model_dump(
                by_alias=True,
                mode='json',
            )

        # `req_model` yoxdursa, o zaman `*args` boş olmalıdır, çünki onların key-ləri bilinmir
        assert not args

        return kwds


class UpdateClosedReceiptHandler(_UpdateReceiptHandler):
    def __init__(
        self,
        req_model=UpdateClosedReceiptRequest,
        resp_model=ObjectResponse[Receipt],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class CloseReceiptHandler(_UpdateReceiptHandler):
    def __init__(
        self,
        req_model=CloseReceiptRequest,
        resp_model=ObjectResponse[Receipt],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)


class GetReceiptStockOperationsHandler(AuthedAPIPayloadHandler):
    def __init__(
        self,
        req_model=ByIDRequest,
        resp_model=ObjectListResponse[ReceiptStockOperation],
        dry=False,
    ):
        super().__init__(req_model, resp_model, dry)
