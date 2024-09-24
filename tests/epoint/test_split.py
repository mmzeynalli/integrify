from integrify.epoint.schemas.parts import EPointTransactionStatus
from integrify.epoint.sync.split import (
    EPointSplitPayAndSaveCardRequest,
    EPointSplitPaymentRequest,
    EPointSplitPayWithSavedCardRequest,
)


def test_epoint_split_payment_request(epoint_mock_split_payment_response):
    resp = EPointSplitPaymentRequest(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
    )(epoint_mock_split_payment_response)

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.redirect_url


def test_epoint_split_pay_with_saved_card_request(epoint_mock_split_pay_with_saved_card_response):
    resp = EPointSplitPayWithSavedCardRequest(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
        card_id='cexxxxxx',
    )(epoint_mock_split_pay_with_saved_card_response)

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.transaction


def test_epoint_split_pay_and_save_card_request(epoint_mock_split_pay_and_save_card_response):
    resp = EPointSplitPayAndSaveCardRequest(
        amount=100,
        currency='AZN',
        order_id='123456789',
        split_user_id='epoint_user_id',
        split_amount=50,
    )(epoint_mock_split_pay_and_save_card_response)

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.redirect_url
    assert resp.body.transaction
    assert resp.body.card_id
