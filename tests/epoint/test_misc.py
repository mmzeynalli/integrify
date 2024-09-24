from integrify.epoint.schemas.parts import EPointTransactionStatus, EPointTransctionStatusExtended
from integrify.epoint.sync.misc import EPointGetTransactionStatusRequest, EPointSaveCardRequest


def test_ok_signature(epoint_mock_get_transaction_status_response):
    resp = EPointGetTransactionStatusRequest(transaction_id='te002458186')(
        epoint_mock_get_transaction_status_response
    )

    assert resp.body.status == EPointTransctionStatusExtended.SUCCESS


def test_wrong_signature(epoint_set_wrong_env, epoint_mock_get_transaction_status_response):
    resp = EPointGetTransactionStatusRequest(transaction_id='te002458186')(
        epoint_mock_get_transaction_status_response
    )

    assert resp.ok
    assert resp.body.status == EPointTransctionStatusExtended.SERVER_ERROR
    assert resp.body.message == 'Signature did not match'


def test_epoint_save_card_request(epoint_mock_save_card_response):
    resp = EPointSaveCardRequest()(epoint_mock_save_card_response)

    assert resp.body.status == EPointTransactionStatus.SUCCESS
    assert resp.body.card_id
