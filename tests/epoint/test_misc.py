from integrify.epoint.schemas.parts import TransactionStatus, TransactionStatusExtended
from integrify.epoint.sync.misc import GetTransactionStatusRequest, SaveCardRequest


def test_ok_signature(epoint_mock_get_transaction_status_response):
    resp = GetTransactionStatusRequest(transaction_id='te002458186')(
        epoint_mock_get_transaction_status_response
    )

    assert resp.body.status == TransactionStatusExtended.SUCCESS


def test_wrong_signature(epoint_set_wrong_env, epoint_mock_get_transaction_status_response):
    resp = GetTransactionStatusRequest(transaction_id='te002458186')(
        epoint_mock_get_transaction_status_response
    )

    assert resp.ok
    assert resp.body.status == TransactionStatusExtended.SERVER_ERROR
    assert resp.body.message == 'Signature did not match'


def test_epoint_save_card_request(epoint_mock_save_card_response):
    resp = SaveCardRequest()(epoint_mock_save_card_response)

    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.card_id
