from functools import partial

import pytest

from integrify.clopos.schemas.common.response import ObjectResponse
from integrify.clopos.schemas.orders.object import Order
from integrify.schemas import APIResponse
from integrify.test import pytest_addoption  # noqa: F401
from integrify.test import requires_env as _requires_env
from tests.client import CloposTestClientClass
from tests.mocks import *  # noqa: F403

requires_env = partial(
    _requires_env,
    'CLOPOS_CLIENT_ID',
    'CLOPOS_CLIENT_SECRET',
    'CLOPOS_BRAND',
    'CLOPOS_INTEGRATOR_ID',
)


@pytest.fixture(scope='package')
def client():
    from tests.client import CloposTestClientClass

    yield CloposTestClientClass()


@pytest.fixture(scope='package')
def authed_client(client):
    from tests.client import CloposTestClientClass

    client = CloposTestClientClass()
    client._token = client.auth().body.token
    yield client


@pytest.fixture(scope='package')
def authed_dry_client(client):
    from tests.client import CloposTestClientClass

    client = CloposTestClientClass(dry=True)
    client._token = 'randomtoken'
    yield client


@pytest.fixture(scope='package')
def new_order_resp(authed_client: 'CloposTestClientClass'):
    resp = authed_client.create_order(  # type: ignore[call-overload]
        customer_id=1,
        payload={
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
        meta={
            'comment': '',
            'discount': {'discount_type': 1, 'discount_value': 10},
            'orderTotal': '16.2000',
            'apply_service_charge': True,
            'customer_discount_type': 1,
            'service_charge_value': 0,
        },
    )

    yield resp


@pytest.fixture(scope='package')
def new_order_object(new_order_resp: APIResponse[ObjectResponse[Order]]):
    yield new_order_resp.body.data


@pytest.fixture(scope='package')
def new_receipt_object(authed_client: 'CloposTestClientClass'):
    # Open API v2-də receipt yaratmaq üçün endpoint yoxdur (create/delete silinib).
    # Ona görə receipt-ə əsaslanan testlər üçün mövcud receipt-lərdən birini götürürük.
    resp = authed_client.get_receipts(limit=1)

    assert resp.ok
    assert resp.body.data, 'Test brendində ən azı bir receipt olmalıdır'

    yield resp.body.data[0]
