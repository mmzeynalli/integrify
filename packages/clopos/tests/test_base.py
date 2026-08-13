# Base parts of Clopos: Auth, Venues, Users/Customers, Categories and Station

from typing import TYPE_CHECKING

from integrify.clopos.schemas.categories.object import Category
from integrify.clopos.schemas.common.response import ErrorResponse
from integrify.clopos.schemas.customers.object import Customer, Group
from integrify.clopos.schemas.sales.object import PaymentMethod, SaleType
from integrify.clopos.schemas.stations.object import Station
from integrify.clopos.schemas.users.object import User
from integrify.clopos.schemas.venues.object import Venue
from tests.conftest import requires_env

if TYPE_CHECKING:
    from tests.client import CloposTestClientClass


@requires_env()
def test_auth(client: 'CloposTestClientClass'):
    resp = client.auth()

    assert resp.ok
    assert resp.body.success
    assert resp.body.token.startswith('oauth_')


@requires_env()
def test_wrong_auth(client: 'CloposTestClientClass'):
    resp = client.auth(brand='wrong_brand')

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success


@requires_env()
def test_get_venues(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_venues()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Venue)


@requires_env()
def test_get_users(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_users()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], User)


@requires_env()
def test_get_user_by_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_user_by_id(1)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, User)

    assert resp.body.data.id == 1


@requires_env()
def test_get_user_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_user_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert resp.body.error[0].message == 'No query results for model [App\\Models\\Auth\\User] 1000'
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_create_customer(authed_client: 'CloposTestClientClass'):
    resp = authed_client.create_customer(
        name='John Doe',
        email='john.doe@example.com',
        # Skip next two fields, as they need to be unique each time
        # phone='+994555555552',
        # code='CUST004',
        description='Test Customer',
        group_id=1,
        gender=1,
        date_of_birth='1990-05-15',
    )

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Customer)
    assert resp.body.data.name == 'John Doe'


@requires_env()
def test_get_customers(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_customers()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Customer)


@requires_env()
def test_get_customer_by_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_customer_by_id(1)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Customer)

    assert resp.body.data.id == 1


@requires_env()
def test_get_customer_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_customer_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\Marketing\\Customer] 1000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_get_customer_groups(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_customer_groups()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Group)


@requires_env()
def test_get_categories(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_categories()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Category)


@requires_env()
def test_get_category_by_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_category_by_id(3)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Category)

    assert resp.body.data.id == 3


@requires_env()
def test_get_category_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_category_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\Category] 1000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_get_stations(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_stations()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Station)


@requires_env()
def test_get_station_by_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_station_by_id(2)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Station)

    assert resp.body.data.id == 2


@requires_env()
def test_get_station_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_station_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\Station] 1000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_get_sale_types(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_sale_types()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], SaleType)


@requires_env()
def test_get_payment_methods(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_payment_methods()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], PaymentMethod)
