from httpx import Response
from pytest_mock import MockFixture

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


def test_get_detail_order_info_wrong_order_id(kapital_client: KapitalClientClass):
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


def test_refund_order(
    kapital_client: KapitalClientClass,
    kapital_mock_refund_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch('httpx.Client.request', return_value=kapital_mock_refund_success_response):
        resp = kapital_client.refund_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.approval_code == 'refund_123'
        assert resp.body.data.pmo_result_code == '1000'


def test_full_reverse_order(
    kapital_client: KapitalClientClass,
    kapital_mock_full_reverse_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request', return_value=kapital_mock_full_reverse_success_response
    ):
        resp = kapital_client.full_reverse_order(order_id=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == '1000'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_clearing_order(
    kapital_client: KapitalClientClass,
    kapital_mock_clearing_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch('httpx.Client.request', return_value=kapital_mock_clearing_success_response):
        resp = kapital_client.clearing_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == '1000'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_partial_reverse_order(
    kapital_client: KapitalClientClass,
    kapital_mock_partial_reverse_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_partial_reverse_success_response,
    ):
        resp = kapital_client.partial_reverse_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == '1000'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_order_with_saved_card(
    kapital_client: KapitalClientClass,
    kapital_mock_order_with_saved_card_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_order_with_saved_card_success_response,
    ):
        resp = kapital_client.order_with_saved_card(amount=1, currency='AZN', description='test')

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.id == 1231
        assert resp.body.data.password == '1231231'


def test_link_card_token(
    kapital_client: KapitalClientClass,
    kapital_mock_link_card_token_success_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_link_card_token_success_response,
    ):
        resp = kapital_client.link_card_token(token=123, order_id=1231, password='1231231')

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.status == 'PreAuth'
        assert resp.body.data.cvv2_auth_status == 'test'
