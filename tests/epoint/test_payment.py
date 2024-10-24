from httpx import Response
from integrify.epoint.client import EPointClientClass
from integrify.epoint.schemas.parts import TransactionStatus
from pytest_mock import MockerFixture


def test_epoint_payment_request(
    epoint_client: EPointClientClass,
    epoint_mock_payment_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch('httpx.Client.request', return_value=epoint_mock_payment_response):
        resp = epoint_client.pay(
            amount=1,
            currency='AZN',
            order_id='123456789',
        )

        assert resp.body.status == TransactionStatus.SUCCESS
        assert resp.body.redirect_url
        assert resp.body.transaction


def test_epoint_pay_with_saved_card_request(
    epoint_client: EPointClientClass,
    epoint_mock_pay_with_saved_card_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_pay_with_saved_card_response,
    ):
        resp = epoint_client.pay_with_saved_card(
            amount=1,
            currency='AZN',
            order_id='123456789',
            card_id='cexxxxxx',
        )
        assert resp.body.status == TransactionStatus.SUCCESS
        assert resp.body.transaction


def test_epoint_pay_and_save_card_request(
    epoint_client: EPointClientClass,
    epoint_mock_pay_and_save_card_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch('httpx.Client.request', return_value=epoint_mock_pay_and_save_card_response):
        resp = epoint_client.pay_and_save_card(
            amount=1,
            currency='AZN',
            order_id='test',
        )

        assert resp.body.status == TransactionStatus.SUCCESS
        assert resp.body.transaction
        assert resp.body.card_id


def test_epoint_payout_request(
    epoint_client: EPointClientClass,
    epoint_mock_payout_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch('httpx.Client.request', return_value=epoint_mock_payout_response):
        resp = epoint_client.payout(
            amount=1,
            currency='AZN',
            order_id='test',
            card_id='cexxxxxx',
        )

        assert resp.body.status == TransactionStatus.SUCCESS
        assert resp.body.transaction


def test_epoint_refund_request(
    epoint_client: EPointClientClass,
    epoint_mock_refund_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch('httpx.Client.request', return_value=epoint_mock_refund_response):
        resp = epoint_client.refund(
            transaction_id='texxxxxx',
            currency='AZN',
        )

        assert resp.body.status == TransactionStatus.SUCCESS
