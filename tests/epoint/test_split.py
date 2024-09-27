from integrify.epoint.schemas.parts import TransactionStatus
from tests.epoint.conftest import TestEPointRequest


def test_epoint_split_payment_request(epoint_mock_split_payment_response):
    resp = TestEPointRequest(epoint_mock_split_payment_response).split_pay(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.redirect_url


def test_epoint_split_pay_with_saved_card_request(epoint_mock_split_pay_with_saved_card_response):
    resp = TestEPointRequest(
        epoint_mock_split_pay_with_saved_card_response
    ).split_pay_with_saved_card(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
        card_id='cexxxxxx',
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.transaction


def test_epoint_split_pay_and_save_card_request(epoint_mock_split_pay_and_save_card_response):
    resp = TestEPointRequest(epoint_mock_split_pay_and_save_card_response).split_pay_and_save_card(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
    )

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.redirect_url
    assert resp.body.transaction
    assert resp.body.card_id
