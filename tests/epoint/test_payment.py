from integrify.epoint.schemas.parts import TransactionStatus

from tests.epoint.conftest import TestEPointRequest


def test_epoint_payment_request(epoint_mock_payment_response):
    resp = TestEPointRequest(epoint_mock_payment_response).pay(
        amount=1,
        currency='AZN',
        order_id='123456789',
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.redirect_url
    assert resp.body.transaction


def test_epoint_pay_with_saved_card_request(epoint_mock_pay_with_saved_card_response):
    resp = TestEPointRequest(epoint_mock_pay_with_saved_card_response).pay_with_saved_card(
        amount=1,
        currency='AZN',
        order_id='123456789',
        card_id='card_id',
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.transaction


def test_epoint_pay_and_save_card_request(epoint_mock_pay_and_save_card_response):
    resp = TestEPointRequest(epoint_mock_pay_and_save_card_response).pay_and_save_card(
        amount=1,
        currency='AZN',
        order_id='test',
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.transaction
    assert resp.body.card_id
