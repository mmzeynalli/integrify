import pytest
from httpx import Response
from pytest_mock import MockFixture

from integrify.kapital.client import KapitalClientClass
from integrify.kapital.schemas.enums import ErrorCode


@pytest.mark.live
def test_create_order_request(kapital_order):
    assert kapital_order.redirect_url.startswith('https://txpgtst.kapitalbank.az')


def test_mock_create_order_request(
    kapital_client: KapitalClientClass,
    kapital_mock_create_order_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_create_order_response,
    ):
        resp = kapital_client.create_order(amount=1, currency='AZN', description='test')

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.id == 1231
        assert resp.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')


@pytest.mark.live
def test_get_order_information_request(
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


@pytest.mark.live
def test_get_order_information_invalid_id_request(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.get_order_information(order_id=0)

    assert resp.body.error is not None, 'Response error is None'

    assert resp.status_code == 500
    assert resp.body.error.error_code == ErrorCode.SERVICE_ERROR
    assert resp.body.error.error_description == 'no order found'


def test_mock_get_order_information_invalid_id_request(
    kapital_client: KapitalClientClass,
    kapital_mock_get_order_info_invalid_id_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_get_order_info_invalid_id_response,
    ):
        resp = kapital_client.get_detailed_order_info(order_id=1)

        assert resp.body.error is not None, 'Response error is None'

        assert resp.body.error.error_code == ErrorCode.SERVICE_ERROR
        assert resp.body.error.error_description == 'no order found'


@pytest.mark.live
def test_get_detailed_order_information_request(
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


@pytest.mark.live
def test_get_detailed_order_information_invalid_id_request(
    kapital_client: KapitalClientClass,
):
    resp = kapital_client.get_detailed_order_info(order_id=0)

    assert resp.body.error is not None, 'Response error is None'

    assert resp.status_code == 500
    assert resp.body.error.error_code == ErrorCode.SERVICE_ERROR
    assert resp.body.error.error_description == 'no order found'


def test_mock_get_detailed_order_information_invalid_id_request(
    kapital_client: KapitalClientClass,
    kapital_mock_get_detail_order_info_invalid_id_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_get_detail_order_info_invalid_id_response,
    ):
        resp = kapital_client.get_detailed_order_info(order_id=1)

        assert resp.body.error is not None, 'Response error is None'

        assert resp.body.error.error_code == ErrorCode.SERVICE_ERROR
        assert resp.body.error.error_description == 'no order found'


@pytest.mark.live
def test_save_card_request(
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


def test_mock_save_card_request(
    kapital_client: KapitalClientClass,
    kapital_mock_save_card_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_save_card_response,
    ):
        resp = kapital_client.save_card(
            amount=1,
            currency='AZN',
            description='test',
        )

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.id == 1231
        assert resp.body.data.password == '1231231'
        assert resp.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')


@pytest.mark.live
def test_pay_and_save_card_request(
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


def test_mock_pay_and_save_card_request(
    kapital_client: KapitalClientClass,
    kapital_mock_pay_and_save_card_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_pay_and_save_card_response,
    ):
        resp = kapital_client.pay_and_save_card(
            amount=1,
            currency='AZN',
            description='test',
        )

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.id == 1231
        assert resp.body.data.password == '1231231'
        assert resp.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')


def test_refund_order_request(
    kapital_client: KapitalClientClass,
    kapital_mock_refund_response: Response,
    mocker: MockFixture,
):
    with mocker.patch('httpx.Client.request', return_value=kapital_mock_refund_response):
        resp = kapital_client.refund_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.approval_code == 'refund_123'
        assert resp.body.data.pmo_result_code == 'No sharing'


def test_full_reverse_order_request(
    kapital_client: KapitalClientClass,
    kapital_mock_full_reverse_response: Response,
    mocker: MockFixture,
):
    with mocker.patch('httpx.Client.request', return_value=kapital_mock_full_reverse_response):
        resp = kapital_client.full_reverse_order(order_id=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == 'No sharing'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_clearing_order_request(
    kapital_client: KapitalClientClass,
    kapital_mock_clearing_response: Response,
    mocker: MockFixture,
):
    with mocker.patch('httpx.Client.request', return_value=kapital_mock_clearing_response):
        resp = kapital_client.clearing_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == 'No sharing'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_partial_reverse_order_request(
    kapital_client: KapitalClientClass,
    kapital_mock_partial_reverse_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_partial_reverse_response,
    ):
        resp = kapital_client.partial_reverse_order(order_id=1, amount=1)

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.pmo_result_code == 'No sharing'
        assert resp.body.data.match.rid_by_pmo == '123'


def test_order_with_saved_card_request(
    kapital_client: KapitalClientClass,
    kapital_mock_order_with_saved_card_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_order_with_saved_card_response,
    ):
        resp = kapital_client.order_with_saved_card(amount=1, currency='AZN', description='test')

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.id == 1231
        assert resp.body.data.password == '1231231'


def test_link_card_token_request(
    kapital_client: KapitalClientClass,
    kapital_mock_link_card_token_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=kapital_mock_link_card_token_response,
    ):
        resp = kapital_client.link_card_token(token=123, order_id=1231, password='1231231')

        assert resp.body.data is not None, 'Response data is None'

        assert resp.body.data.status == 'PreAuth'
        assert resp.body.data.cvv2_auth_status == 'test'
