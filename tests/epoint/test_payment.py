from integrify.epoint.schemas.parts import EPointTransactionStatus
from integrify.epoint.sync.payment import (
    EPointPayAndSaveCardRequest,
    EPointPaymentRequest,
    EPointPayWithSavedCardRequest,
)


def test_epoint_payment_request(epoint_mock_payment_response):
    resp = EPointPaymentRequest(amount=1, currency='AZN', order_id='123456789')(
        epoint_mock_payment_response
    )

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.redirect_url
    assert resp.body.transaction


def test_epoint_pay_with_saved_card_request(epoint_mock_pay_with_saved_card_response):
    resp = EPointPayWithSavedCardRequest(
        amount=1,
        currency='AZN',
        order_id='123456789',
        card_id='card_id',
    )(epoint_mock_pay_with_saved_card_response)

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.transaction


def test_epoint_pay_and_save_card_request(epoint_mock_pay_and_save_card_response):
    resp = EPointPayAndSaveCardRequest(amount=1, currency='AZN', order_id='test')(
        epoint_mock_pay_and_save_card_response
    )

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.transaction
    assert resp.body.card_id
