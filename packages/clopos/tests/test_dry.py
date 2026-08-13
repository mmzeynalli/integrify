import json

import pytest

from tests.client import CloposTestClientClass


@pytest.mark.parametrize('selects', [['id', 'name'], 'id,name'])
def test_get_products_dry(authed_dry_client: 'CloposTestClientClass', selects):
    resp = authed_dry_client.get_products(selects=selects, filters={'giftable': 1})

    assert isinstance(resp, dict)
    assert 'data' in resp
    assert isinstance(resp['data'], str)

    resp_data = json.loads(resp['data'])
    assert 'selects[]' in resp_data
    assert 'filters' in resp_data

    assert resp_data['selects[]'] == 'id,name'
    assert resp_data['filters'] == {'giftable': ['giftable', 1]}


def test_get_product_by_id_dry(authed_dry_client: 'CloposTestClientClass'):
    resp = authed_dry_client.get_product_by_id(1, with_=['modifications', 'modificator_groups'])

    assert isinstance(resp, dict)
    assert 'data' in resp
    assert isinstance(resp['data'], dict)

    assert resp['data'] == {'with[]': ['modifications', 'modificator_groups']}


def test_get_stop_list_dry(authed_dry_client: 'CloposTestClientClass'):
    resp = authed_dry_client.get_stop_list(
        filters=[
            {'by': 'id', 'from_': '0', 'to': '100'},
            {'by': 'limit', 'from_': '1', 'to': '10'},
        ]
    )

    assert isinstance(resp, dict)
    assert 'data' in resp
    assert isinstance(resp['data'], dict)

    assert resp['data'] == {
        'filters[0][0]': 'id',
        'filters[0][1][0]': 0,
        'filters[0][1][1]': 100,
        'filters[1][0]': 'limit',
        'filters[1][1][0]': 1,
        'filters[1][1][1]': 10,
    }


def test_get_customers_dry(authed_dry_client: 'CloposTestClientClass'):
    resp = authed_dry_client.get_customers(
        with_=['group', 'balance'],
        filters=[
            {'by': 'name', 'value': 'John Doe'},
            {'by': 'phones', 'value': '+1234567890'},
        ],
    )

    assert isinstance(resp, dict)
    assert 'data' in resp
    assert isinstance(resp['data'], dict)
    assert resp['data'] == {
        'with[0]': 'group',
        'with[1]': 'balance',
        'filters[0][0]': 'name',
        'filter[0][1]': 'John Doe',
        'filters[1][0]': 'phones',
        'filter[1][1]': '+1234567890',
    }
