from collections.abc import Coroutine
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Generic, Literal, overload

from integrify.api import APIClient, _Async, _Mode, _Sync
from integrify.clopos import env
from integrify.clopos.handlers import (
    AuthHandler,
    CloseReceiptHandler,
    CreateCustomerHandler,
    CreateOrderHandler,
    GetByIDHandler,
    GetCategoriesHandler,
    GetCategoryByIDHandler,
    GetCustomersHandler,
    GetOrderByIDHandler,
    GetOrdersHandler,
    GetPaginatedDataHandler,
    GetProductByIDHandler,
    GetProductsHandler,
    GetReceiptsHandler,
    GetReceiptStockOperationsHandler,
    GetStationsHandler,
    GetStopListHandler,
    UpdateClosedReceiptHandler,
    UpdateOrderHandler,
)
from integrify.clopos.schemas.auth.response import AuthResponse
from integrify.clopos.schemas.categories.object import Category
from integrify.clopos.schemas.common.response import (
    ObjectListResponse,
    ObjectResponse,
)
from integrify.clopos.schemas.customers.object import Customer, Group
from integrify.clopos.schemas.customers.request import CustomerFilter
from integrify.clopos.schemas.enums import (
    CategoryType,
    Gender,
    OrderStatus,
)
from integrify.clopos.schemas.orders.object import Order, OrderPayloadIn
from integrify.clopos.schemas.price_lists.object import PriceList, PriceListPrice
from integrify.clopos.schemas.products.object import Product, StopList
from integrify.clopos.schemas.products.request import GetProducstRequestFilter, StopListFilter
from integrify.clopos.schemas.receipts.object import (
    Receipt,
    ReceiptStockOperation,
)
from integrify.clopos.schemas.receipts.request import PaymentMethodIn
from integrify.clopos.schemas.sales.object import PaymentMethod, SaleType
from integrify.clopos.schemas.stations.object import Station
from integrify.clopos.schemas.users.object import User
from integrify.clopos.schemas.venues.object import Venue
from integrify.schemas import APIResponse
from integrify.utils import UNSET, Unset

__all__ = ['CloposClientClass', 'CloposRequest', 'CloposAsyncRequest']


class CloposClientClass(APIClient, Generic[_Mode]):
    """Base class for CloposClient"""

    def __init__(
        self,
        name='Clopos',
        base_url: str | None = env.API.BASE_URL,
        default_handler=None,
        sync: bool = True,
        dry: bool = False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('auth', env.API.AUTH, verb='POST')
        self.add_handler('auth', AuthHandler)

        self.add_url('get_venues', env.API.VENUES, verb='GET')
        self.add_handler('get_venues', GetPaginatedDataHandler(Venue))

        self.add_url('get_users', env.API.USERS, verb='GET')
        self.add_handler('get_users', GetPaginatedDataHandler(User))
        self.add_url('get_user_by_id', env.API.USER_BY_ID, verb='GET')
        self.add_handler('get_user_by_id', GetByIDHandler(User))

        self.add_url('get_customers', env.API.CUSTOMERS, verb='GET')
        self.add_handler('get_customers', GetCustomersHandler)
        self.add_url('get_customer_by_id', env.API.CUSTOMER_BY_ID, verb='GET')
        self.add_handler('get_customer_by_id', GetByIDHandler(Customer))
        self.add_url('create_customer', env.API.CUSTOMERS, verb='POST')
        self.add_handler('create_customer', CreateCustomerHandler)
        self.add_url('get_customer_groups', env.API.CUSTOMER_GROUPS, verb='GET')
        self.add_handler('get_customer_groups', GetPaginatedDataHandler(Group))

        self.add_url('get_categories', env.API.CATEGORIES, verb='GET')
        self.add_handler('get_categories', GetCategoriesHandler)
        self.add_url('get_category_by_id', env.API.CATEGORY_BY_ID, verb='GET')
        self.add_handler('get_category_by_id', GetCategoryByIDHandler)

        self.add_url('get_stations', env.API.STATIONS, verb='GET')
        self.add_handler('get_stations', GetStationsHandler)
        self.add_url('get_station_by_id', env.API.STATION_BY_ID, verb='GET')
        self.add_handler('get_station_by_id', GetByIDHandler(Station))

        self.add_url('get_products', env.API.PRODUCTS, verb='GET')
        self.add_handler('get_products', GetProductsHandler)
        self.add_url('get_product_by_id', env.API.PRODUCT_BY_ID, verb='GET')
        self.add_handler('get_product_by_id', GetProductByIDHandler)
        self.add_url('get_stop_list', env.API.STOP_LIST, verb='GET')
        self.add_handler('get_stop_list', GetStopListHandler)

        self.add_url('get_sale_types', env.API.SALE_TYPES, verb='GET')
        self.add_handler('get_sale_types', GetPaginatedDataHandler(SaleType))
        self.add_url('get_payment_methods', env.API.PAYMENT_METHODS, verb='GET')
        self.add_handler('get_payment_methods', GetPaginatedDataHandler(PaymentMethod))

        self.add_url('get_orders', env.API.ORDERS, verb='GET')
        self.add_handler('get_orders', GetOrdersHandler)
        self.add_url('get_order_by_id', env.API.ORDER_BY_ID, verb='GET')
        self.add_handler('get_order_by_id', GetOrderByIDHandler)
        self.add_url('create_order', env.API.ORDERS, verb='POST')
        self.add_handler('create_order', CreateOrderHandler)
        self.add_url('update_order', env.API.ORDER_BY_ID, verb='PUT')
        self.add_handler('update_order', UpdateOrderHandler)

        self.add_url('get_receipts', env.API.RECEIPTS, verb='GET')
        self.add_handler('get_receipts', GetReceiptsHandler)
        self.add_url('get_receipt_by_id', env.API.RECEIPT_BY_ID, verb='GET')
        self.add_handler('get_receipt_by_id', GetByIDHandler(Receipt))
        self.add_url('update_closed_receipt', env.API.RECEIPT_BY_ID, verb='PATCH')
        self.add_handler('update_closed_receipt', UpdateClosedReceiptHandler)
        self.add_url('close_receipt', env.API.RECEIPT_CLOSE, verb='POST')
        self.add_handler('close_receipt', CloseReceiptHandler)
        self.add_url('get_receipt_stock_operations', env.API.RECEIPT_STOCK_OPERATIONS, verb='GET')
        self.add_handler('get_receipt_stock_operations', GetReceiptStockOperationsHandler)

        self.add_url('get_price_lists', env.API.PRICE_LISTS, verb='GET')
        self.add_handler('get_price_lists', GetPaginatedDataHandler(PriceList))
        self.add_url('get_price_list_prices', env.API.PRICE_LIST_PRICES, verb='GET')
        self.add_handler('get_price_list_prices', GetPaginatedDataHandler(PriceListPrice))

    def _build_request_lambda(self, func, url, verb, handler):
        # No headers needed in auth
        if url.endswith(env.API.AUTH):
            return super()._build_request_lambda(func, url, verb, handler)

        return lambda *args, headers, **kwds: func(
            url,
            verb,
            handler,
            *(arg for arg in args if arg is not UNSET),
            headers=headers,
            **{k: v for k, v in kwds.items() if v is not UNSET},
        )

    if TYPE_CHECKING:
        # pylint: disable=all
        @overload
        def auth(
            self: 'CloposClientClass[_Sync]',
            client_id: Unset[str] = UNSET,
            client_secret: Unset[str] = UNSET,
            brand: Unset[str] = UNSET,
            integrator_id: Unset[str] = UNSET,
        ) -> APIResponse[AuthResponse]:
            """Exchange your client credentials for a short-lived access token that authorizes all other API requests.


            **Endpoint**: `POST /open-api/v2/auth`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.auth(
                client_id='eNUKI04aYJRU6TBhh5bwUrvmEORgQoxM',
                client_secret='dqYkWUpDjzvKOgbP3ar8tSNKJbwMyYe1V5R7DHClfSNYkap5C5XxRA6PmzoPv1I2',
                brand='openapitest',
                integrator_id='1'
            )

            # Or if you have set the environment variables
            CloposClient.auth(headers={'x-token': 'token'})
            ```

            **Response format: [`AuthResponse`][integrify.clopos.schemas.auth.response.AuthResponse]**

            This request returns you a token for subsequent API calls which is valid for one hour.

            Args:
                client_id: Client ID provided by Clopos. Can be set in environment variable `CLOPOS_CLIENT_ID`
                client_secret: Client secret provided by Clopos. Can be set in environment variable `CLOPOS_CLIENT_SECRET`
                brand: Brand you want to authenticate. Can be set in environment variable `CLOPOS_BRAND`
                integrator_id: Integrator ID provided by Clopos. Can be set in environment variable `CLOPOS_INTEGRATOR_ID`
            """  # noqa: E501

        @overload
        def auth(
            self: 'CloposClientClass[_Async]',
            client_id: Unset[str] = UNSET,
            client_secret: Unset[str] = UNSET,
            brand: Unset[str] = UNSET,
            integrator_id: Unset[str] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[AuthResponse]]: ...
        def auth(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_venues(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Venue]]:
            """Allows you to quickly retrieve active branches connected to your brand to initiate location-based operations.

            **Endpoint**: `GET /open-api/venues`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_venues(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_venues(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Venue]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_venues(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Venue]]]: ...
        def get_venues(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_users(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[User]]:
            """Use this endpoint to inspect staff accounts, roles, and access levels across your venues.

            **Endpoint**: `GET /open-api/users`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_users(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_users(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[User]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_users(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[User]]]: ...
        def get_users(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_user_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[User]]:
            """Retrieve a specific user by their unique identifier.

            **Endpoint**: `GET /open-api/users/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_user_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_user_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[User]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: User ID
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_user_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[User]]]: ...
        def get_user_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_customers(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            with_: Unset[list[str]] = UNSET,
            filters: Unset[list[CustomerFilter]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Customer]]:
            """Retrieve all customers with optional search, pagination, filtering, and relationship inclusion

            **Endpoint**: `GET /open-api/customers`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_customers(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_customers(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Customer]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                with_: Include related data in the response. Supported values: `group`, `balance`, cashback_balance. You can include multiple with parameters.
                filters: List of filters to apply in format {'by': 'name'|'phones'|'group_id', 'value': str}
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_customers(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            with_: Unset[list[str]] = UNSET,
            filters: Unset[list[CustomerFilter]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Customer]]]: ...
        def get_customers(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_customer_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Customer]]:
            """Retrieve a specific customer by their unique identifier.

            **Endpoint**: `GET /open-api/customers/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_customer_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_customer_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Customer]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Customer ID
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_customer_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Customer]]]: ...
        def get_customer_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def create_customer(
            self: 'CloposClientClass[_Sync]',
            name: str,
            email: Unset[str] = UNSET,
            phone: Unset[str] = UNSET,
            code: Unset[str] = UNSET,
            cid: Unset[str] = UNSET,
            description: Unset[str] = UNSET,
            group_id: Unset[int] = UNSET,
            gender: Unset[Gender] = UNSET,
            date_of_birth: Unset[str | date] = UNSET,
            header: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Customer]]:
            """Create a new customer with contact information and group assignment

            **Endpoint**: `POST /open-api/customers`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.create_customer(name='John Doe', email='random@example.com', headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.create_customer(name='John Doe', email='random@example.com', headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Customer]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                name: Customer name
                email: Customer email
                phone: Customer phone (must be unique)
                code: Customer code (must be unique)
                cid: Customer CID
                description: Customer description
                group_id: Customer group ID
                gender: Customer gender
                date_of_birth: Customer date of birth in format YYYY-MM-DD
                header: Headers for request
            ```
            """  # noqa: E501

        @overload
        def create_customer(
            self: 'CloposClientClass[_Async]',
            name: str,
            email: Unset[str] = UNSET,
            phone: Unset[str] = UNSET,
            code: Unset[str] = UNSET,
            cid: Unset[str] = UNSET,
            description: Unset[str] = UNSET,
            group_id: Unset[int] = UNSET,
            gender: Unset[Gender] = UNSET,
            date_of_birth: Unset[str | date] = UNSET,
            header: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Customer]]]: ...
        def create_customer(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_customer_groups(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Group]]:
            """Retrieve a list of all customer groups with pagination support.

            **Endpoint**: `GET /open-api/customer-groups`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_customer_groups(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_customer_groups(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Group]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_customer_groups(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Group]]]: ...
        def get_customer_groups(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_categories(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            parent_id: Unset[int] = UNSET,
            type: Unset[CategoryType] = UNSET,
            include_children: Unset[bool] = True,
            include_inactive: Unset[bool] = False,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Category]]:
            """Retrieve product categories along with their hierarchical structure

            **Endpoint**: `GET /open-api/categories`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_categories(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_categories(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Category]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Number of categories to return (1-999)
                parent_id: Filters records under a specific parent category
                type: Category type; PRODUCT, INGREDIENT, ACCOUNTING
                include_children: Include child categories in the response
                include_inactive: Include inactive categories
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_categories(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            parent_id: Unset[int] = UNSET,
            type: Unset[CategoryType] = UNSET,
            include_children: Unset[bool] = True,
            include_inactive: Unset[bool] = False,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Category]]]: ...
        def get_categories(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_category_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Category]]:
            """Retrieve a specific menu category with its hierarchical details

            **Endpoint**: `GET /open-api/categories/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_category_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_category_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Category]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Category ID
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_category_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Category]]]: ...
        def get_category_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_stations(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            status: Unset[int] = UNSET,
            can_print: Unset[bool] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Station]]:
            """Retrieve all preparation and service stations

            **Endpoint**: `GET /open-api/stations`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_stations(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_stations(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Station]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-200)
                status: Filter by station status (`1` = active, `0` = inactive)
                can_print: Filter stations that can redirect to a printer.
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_stations(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            status: Unset[int] = UNSET,
            can_print: Unset[bool] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Station]]]: ...
        def get_stations(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_station_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Station]]:
            """Retrieve a specific preparation or service station

            **Endpoint**: `GET /open-api/stations/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_station_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_station_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Station]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Station ID
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_station_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Station]]]: ...
        def get_station_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_products(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            selects: Unset[str | list[str]] = UNSET,
            filters: Unset[GetProducstRequestFilter] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Product]]:
            """Get the product catalog with advanced filtering and pagination.

            **Endpoint**: `GET /open-api/products`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_products(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_products(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Product]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                selects: Comma-separated string OR list of fields to include in the response. The fields id, name, and type are always included regardless of this parameter. \
                Example: selects=id,name,type,price,image
                filters:
                    - type: Filters by product type. Possible values: GOODS, DISH, TIMER, PREPARATION, INGREDIENT
                    - category_id: Lists products belonging to the specified category IDs
                    - station_id: Retrieves products assigned to the specified station IDs
                    - tags: Filters for products with the specified tag IDs
                    - giftable: Filters for products that are ("1") or are not giftable. Possible values: 1, 0, true, false
                    - discountable: Filters for products that are ("1") or are not discountable. Possible values: 1, 0, true, false
                    - inventory_behavior: Filters by inventory behavior mode (e.g., "3")
                    - have_ingredients: Retrieves products that have a recipe/ingredients ("1"). Possible values: 1, 0, true, false
                    - sold_by_portion: Lists products sold by portion ("1"). Possible values: 1, 0, true, false
                    - has_variants: Lists products that have variants (modifications) ("1"). Possible values: 1, 0, true, false
                    - has_modifiers: Retrieves products that have a modifier group (modificator_groups) ("1"). Possible values: 1, 0, true, false
                    - has_barcode: Retrieves products that have a barcode ("1"). Possible values: 1, 0, true, false
                    - has_service_charge: Lists products to which a service charge applies ("1"). Possible values: 1, 0, true, false
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_products(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            selects: Unset[str | list[str]] = UNSET,
            filters: Unset[GetProducstRequestFilter] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Product]]]: ...
        def get_products(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_product_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            with_: Unset[list[str]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Product]]:
            """Retrieve a single product with type-specific details.

            **Endpoint**: `GET /open-api/products/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_product_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_product_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Product]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Product ID
                with_: Related data selector. Example: taxes, unit, modifications, modificator_groups, recipe, packages, media, tags, setting. You can include multiple with parameters
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_product_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            with_: Unset[list[str]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Product]]]: ...
        def get_product_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_stop_list(
            self: 'CloposClientClass[_Sync]',
            filters: Unset[list[StopListFilter]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[StopList]]:
            """Get stop list data for specific products.

            You can filter by multiple parameters at once. For that have order of your lists in check.

            **Endpoint**: `GET /open-api/products/stop-list`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_stop_list(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_stop_list(
                filters=[
                    {'by': 'id', 'from_': '0', 'to': '100'},
                    {'by': 'limit', 'from_': '1', 'to': '10'},
                ]
                headers={'x-token': token},
            )  # Filter by id from 0 to 100 AND limit from 1 to 10
            ```

            **Response format: [`ObjectListResponse[StopList]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                filters: List of filter options. Each filter is a dict with keys 'by', 'from_', and 'to'.
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_stop_list(
            self: 'CloposClientClass[_Async]',
            filters: Unset[list[StopListFilter]] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[StopList]]]: ...
        def get_stop_list(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_sale_types(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[SaleType]]:
            """Retrieve a list of all available sale types.

            **Endpoint**: `GET /open-api/sale-types`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_sale_types(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_sale_types(headers={'x-token': 'token'})
            ```

            Used by:
                Create Order: provide payload.service.sale_type_id and payload.service.venue_id
                Create Receipt: optionally include sale_type_id or meta.sale_type

            **Response format: [`ObjectListResponse[SaleType]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_sale_types(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[SaleType]]]: ...
        def get_sale_types(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_payment_methods(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[PaymentMethod]]:
            """Retrieve a list of all configured payment methods.

            **Endpoint**: `GET /open-api/payment-methods`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_payment_methods(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_payment_methods(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[PaymentMethod]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_payment_methods(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[PaymentMethod]]]: ...
        def get_payment_methods(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_orders(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            status: Unset[OrderStatus] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Order]]:
            """Retrieve orders with replicable filters and status-based searches

            **Endpoint**: `GET /open-api/orders`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_orders(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_orders(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Order]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-100)
                status: Filter by order status
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_orders(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 20,
            status: Unset[OrderStatus] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Order]]]: ...
        def get_orders(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_order_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            with_: Unset[Literal['receipt:id', 'service_notification_id', 'status']] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Order]]:
            """Retrieve a single order with status, customer, and line item details.

            **Endpoint**: `GET /open-api/orders/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_order_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_order_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Order]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Order ID
                with_: Include related resources in the response. Currently supported: receipt:id,service_notification_id,status. \
                    When included, the data.receipt field will be present in the response (or null if no receipt exists for the order).
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_order_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            with_: Unset[Literal['receipt:id', 'service_notification_id', 'status']] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Order]]]: ...
        def get_order_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def create_order(
            self: 'CloposClientClass[_Sync]',
            customer_id: int,
            payload: OrderPayloadIn,
            meta: Unset[dict] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Order]]:
            """Create a new order with product line items and customer information

            **Endpoint**: `POST /open-api/orders`

            Example:
            ```python
            from integrify.clopos import CloposClient

            data = {
                    'customer_id': 1,
                    'payload': {
                        'service': {
                            'sale_type_id': 2,
                            'sale_type_name': 'Delivery',
                            'venue_id': 1,
                            'venue_name': 'Main',
                        },
                        'customer': {
                            'id': 9,
                            'name': 'Rahid Akhundzada',
                            'customer_discount_type': 1,
                            'phone': '+994705401040',
                        },
                        'products': [
                            {
                                'product_id': 1,
                                'count': 1,
                                'product_modificators': [
                                    {'modificator_id': 187, 'count': 1},
                                    {'modificator_id': 201, 'count': 1},
                                ],
                                'meta': {
                                    'price': 0,
                                    'order_product': {
                                        'product': {
                                            'id': 1,
                                            'name': 'Mega Dürüm Menü Alana Çiğ Köfte Dürüm',
                                            'category_id': 1,
                                            'station_id': 1,
                                            'price': 0,
                                        },
                                        'count': 1,
                                        'status': 'completed',
                                        'product_modificators': [
                                            {'modificator_id': 187, 'count': 1},
                                            {'modificator_id': 201, 'count': 1},
                                        ],
                                        'product_hash': 'MTExODcsMTEyMDE=',
                                    },
                                },
                            }
                        ],
                    },
                    'meta': {
                        'comment': '',
                        'discount': {'discount_type': 1, 'discount_value': 10},
                        'orderTotal': '16.2000',
                        'apply_service_charge': True,
                        'customer_discount_type': 1,
                        'service_charge_value': 0,
                    },
                }

            CloposClient.create_order(**data, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.create_order(**data, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Order]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Prerequisites:
                - The top-level customer_id must be provided.
                - Service context is required in payload.service:
                - sale_type_id — a valid sale type ID from List Sale Types
                - sale_type_name — human-readable sale type name
                - venue_id and venue_name — the venue where the order will be fulfilled
                - Product and modifier identifiers must exist in the POS catalog. Include the meta.order_product data returned by catalog APIs for accurate reconciliation.
                - Totals and discounts are recalculated by the platform; send the raw values shown to operators.

            Args:
                customer_id: Customer ID
                payload: Order payload
                meta: Meta object
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def create_order(
            self: 'CloposClientClass[_Async]',
            customer_id: int,
            payload: OrderPayloadIn,
            meta: Unset[dict] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Order]]]: ...
        def create_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def update_order(
            self: 'CloposClientClass[_Sync]',
            id: int,
            status: OrderStatus,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Order]]:
            """Update the status of an existing order

            **Endpoint**: `PUT /open-api/orders/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient
            from integrify.clopos.schemas.enums import OrderStatus

            CloposClient.update_order(id=1, OrderStatus.IGNORE, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.update_order(id=1, status=OrderStatus.IGNORE)
            ```

            **Response format: [`ObjectResponse[Order]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Order ID
                status: Order status to update
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def update_order(
            self: 'CloposClientClass[_Async]',
            id: int,
            status: OrderStatus,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Order]]]: ...
        def update_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_receipts(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            sort_by: Unset[str] = 'created_at',
            sort_order: Unset[int] = -1,
            date_from: Unset[str | datetime] = UNSET,
            date_to: Unset[str | datetime] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[Receipt]]:
            """Retrieve all receipts with support for filters and sorting

            **Endpoint**: `GET /open-api/receipts`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_receipts(headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_receipts(headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectListResponse[Receipt]`][integrify.clopos.schemas.common.response.ObjectListResponse]**

            Args:
                page: Page number for pagination (starts at 1)
                limit: Maximum number of objects to return (1-200)
                sort_by: Primary sort field
                sort_order: Primary sort direction (1 = ascending, -1 = descending)
                date_from: Start date (inclusive) in YYYY-MM-DD format
                date_to: End date (inclusive) in YYYY-MM-DD format
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_receipts(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = 1,
            limit: Unset[int] = 50,
            sort_by: Unset[str] = 'created_at',
            sort_order: Unset[int] = -1,
            date_from: Unset[str | datetime] = UNSET,
            date_to: Unset[str | datetime] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[Receipt]]]: ...
        def get_receipts(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_receipt_by_id(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Receipt]]:
            """Retrieve the full details of a specific receipt

            **Endpoint**: `GET /open-api/receipts/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.get_receipt_by_id(1, headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.get_receipt_by_id(id=1, headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Receipt]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Receipt ID
                headers: Headers for request
            ```
            """  # noqa: E501

        @overload
        def get_receipt_by_id(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Receipt]]]: ...
        def get_receipt_by_id(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def update_closed_receipt(
            self: 'CloposClientClass[_Sync]',
            id: int,
            order_status: Unset[OrderStatus] = UNSET,
            order_number: Unset[str] = UNSET,
            fiscal_id: Unset[str] = UNSET,
            lock: Unset[bool] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Receipt]]:
            """Update specific fields of a receipt using the PATCH method. Only the provided fields will be updated; all other fields remain unchanged.

            **Endpoint**: `PATCH /open-api/receipts/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.update_closed_receipt(1, order_status='NEW', headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.update_closed_receipt(id=1, order_status='NEW', headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Receipt]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Receipt ID
                order_status: New order status. Valid values: "NEW", "SCHEDULED", "IN_PROGRESS", "READY", "PICKED_UP", "COMPLETED", "CANCELLED"
                order_number: Order number identifier (e.g., "RPO-00001")
                fiscal_id: Fiscal receipt identifier
                lock: Lock status of the receipt
                headers: Headers for request
            """  # noqa: E501

        @overload
        def update_closed_receipt(
            self: 'CloposClientClass[_Async]',
            id: int,
            order_status: Unset[OrderStatus] = UNSET,
            order_number: Unset[str] = UNSET,
            fiscal_id: Unset[str] = UNSET,
            lock: Unset[bool] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Receipt]]]: ...
        def update_closed_receipt(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def close_receipt(
            self: 'CloposClientClass[_Sync]',
            id: int,
            cid: str,
            payment_methods: list[PaymentMethodIn],
            closed_at: str,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectResponse[Receipt]]:
            """Comprehensively update a receipt using the PUT method. This method allows you to update multiple fields at once and can also be used to close receipts.

            Critical Requirements:
                - The cid and id fields must not change. If different values are sent, the system will treat it as a new receipt and return an error.
                - All fields in the request body must be provided (full receipt object update).

            **Endpoint**: `PUT /open-api/receipts/{id}`

            Example:
            ```python
            from integrify.clopos import CloposClient

            CloposClient.update_closed_receipt(1, order_status='NEW', headers={'x-brand': 'openapitest', 'x-venue': '1', 'x-token': 'token'})

            # Or if you have set the environment variables
            CloposClient.update_closed_receipt(id=1, order_status='NEW', headers={'x-token': 'token'})
            ```

            **Response format: [`ObjectResponse[Receipt]`][integrify.clopos.schemas.common.response.ObjectResponse]**

            Args:
                id: Receipt ID. **Must match the path parameter** - cannot be changed.
                cid: Client identifier. **Must match the existing receipt's CID** - cannot be changed.
                payment_methods: List of payment methods with amounts
                closed_at: Closing timestamp in format "YYYY-MM-DD HH:mm:ss". Must be greater than created_at.
                headers: Headers for request
            """  # noqa: E501

        @overload
        def close_receipt(
            self: 'CloposClientClass[_Async]',
            id: int,
            cid: str,
            payment_methods: list[PaymentMethodIn],
            closed_at: str,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectResponse[Receipt]]]: ...
        def close_receipt(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_receipt_stock_operations(
            self: 'CloposClientClass[_Sync]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[ReceiptStockOperation]]:
            """Retrieve the stock deductions (operations) generated by a receipt.

            **Endpoint**: `GET /open-api/v2/receipts/{id}/stock-operations`

            Args:
                id: The receipt ID (path parameter).
            """  # noqa: E501

        @overload
        def get_receipt_stock_operations(
            self: 'CloposClientClass[_Async]',
            id: int,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[ReceiptStockOperation]]]: ...
        def get_receipt_stock_operations(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_price_lists(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[PriceList]]:
            """Retrieve all configured price lists.

            **Endpoint**: `GET /open-api/v2/price-lists`

            Args:
                page: Page number for pagination.
                limit: Number of items per page (1-999).
            """  # noqa: E501

        @overload
        def get_price_lists(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[PriceList]]]: ...
        def get_price_lists(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_price_list_prices(
            self: 'CloposClientClass[_Sync]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> APIResponse[ObjectListResponse[PriceListPrice]]:
            """Retrieve individual product prices within price lists.

            **Endpoint**: `GET /open-api/v2/price-lists/prices`

            Args:
                page: Page number for pagination.
                limit: Number of items per page (1-999).
            """  # noqa: E501

        @overload
        def get_price_list_prices(
            self: 'CloposClientClass[_Async]',
            page: Unset[int] = UNSET,
            limit: Unset[int] = UNSET,
            *,
            headers: Unset[dict[str, str]] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[ObjectListResponse[PriceListPrice]]]: ...
        def get_price_list_prices(self, *args: Any, **kwds: Any) -> Any: ...


CloposRequest: 'CloposClientClass[_Sync]' = CloposClientClass(sync=True)
CloposAsyncRequest: 'CloposClientClass[_Async]' = CloposClientClass(sync=False)
