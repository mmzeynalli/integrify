from integrify.kapital.client import KapitalClientClass


def test_kapital_create_order(kapital_order):
    assert kapital_order.redirect_url.startswith('https://txpgtst.kapitalbank.az')


def test_get_order_info(
    kapital_order,
    kapital_client: KapitalClientClass,
):
    order_id = kapital_order.id
    resp = kapital_client.get_order_information(order_id=order_id)

    assert resp.body.data is not None, 'Response data is None'

    assert resp.status_code == 200
    assert resp.body.data.id == order_id
    assert resp.body.data.amount == 1
    assert resp.body.data.currency == 'AZN'
    assert resp.body.data.status == 'Preparing'


def test_get_order_info_wrong_order_id(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.get_order_information(order_id=0)

    assert resp.body.error is not None, 'Response error is None'

    assert resp.status_code == 500
    assert resp.body.error.error_code == 'ServiceError'
    assert resp.body.error.error_description == 'no order found'


def test_get_detailed_order_info(
    kapital_order,
    kapital_client: KapitalClientClass,
):
    order_id = kapital_order.id
    resp = kapital_client.get_detailed_order_info(order_id=order_id)

    assert resp.body.data is not None, 'Response data is None'

    assert resp.status_code == 200
    assert resp.body.data.id == order_id
    assert resp.body.data.amount == 1
    assert resp.body.data.currency == 'AZN'
    assert resp.body.data.status == 'Preparing'
    assert resp.body.data.password == kapital_order.password

    assert resp.body.data.hpp_redirect_url is not None, 'Redirect URL is None'
    assert resp.body.data.hpp_redirect_url.startswith('https://txpgtst.kapitalbank.az')


def test_get_detail_order_info_wrong_order_id(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.get_detailed_order_info(order_id=0)

    assert resp.body.error is not None, 'Response error is None'

    assert resp.status_code == 500
    assert resp.body.error.error_code == 'ServiceError'
    assert resp.body.error.error_description == 'no order found'


def test_save_card(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.save_card(
        amount=1,
        currency='AZN',
        description='test',
    )

    assert resp.body.data is not None, 'Response data is None'

    assert resp.status_code == 200
    assert resp.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')


def test_pay_and_save_card(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.pay_and_save_card(
        amount=1,
        currency='AZN',
        description='test',
    )

    assert resp.body.data is not None, 'Response data is None'

    assert resp.status_code == 200
    assert resp.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')
