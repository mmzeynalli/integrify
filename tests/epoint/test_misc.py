import os
from typing import TYPE_CHECKING

from pytest_mock import MockerFixture

from tests.epoint.conftest import requires_env
from tests.epoint.mocks import MESSAGE_TRANSACTION_FAIL

if TYPE_CHECKING:
    from integrify.epoint.client import EPointClientClass


@requires_env('EPOINT_TRANSACTION_ID')
def test_ok_signature(epoint_client: 'EPointClientClass'):
    from integrify.epoint.schemas.enums import TransactionStatusExtended

    resp = epoint_client.get_transaction_status(transaction_id=os.getenv('EPOINT_TRANSACTION_ID'))
    assert resp.ok
    assert resp.body.status == TransactionStatusExtended.RETURNED


@requires_env()
def test_wrong_pubkey(epoint_set_wrong_public_key, epoint_client: 'EPointClientClass'):
    from integrify.epoint.schemas.enums import TransactionStatusExtended

    resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

    assert not resp.ok
    assert resp.body.status == TransactionStatusExtended.SERVER_ERROR
    assert resp.body.message == 'Merchant not found'


@requires_env()
def test_wrong_signature(epoint_set_wrong_private_key, epoint_client: 'EPointClientClass'):
    from integrify.epoint.schemas.enums import TransactionStatusExtended

    resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

    assert not resp.ok
    assert resp.body.status == TransactionStatusExtended.SERVER_ERROR
    assert resp.body.message == 'Signature did not match'


def test_get_failed_transaction_status(
    epoint_mock_get_transaction_status_failed_response,
    epoint_client: 'EPointClientClass',
    mocker: MockerFixture,
):
    from integrify.epoint.schemas.enums import TransactionStatusExtended

    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_get_transaction_status_failed_response,
    ):
        resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

        assert resp.ok
        assert resp.body.status == TransactionStatusExtended.ERROR
        assert resp.body.message == MESSAGE_TRANSACTION_FAIL


@requires_env()
def test_epoint_save_card_request(epoint_client: 'EPointClientClass'):
    from integrify.epoint.schemas.enums import TransactionStatus

    resp = epoint_client.save_card()

    assert resp.ok
    assert resp.body.status == TransactionStatus.SUCCESS
    assert resp.body.card_id


def test_epoint_save_card_failed_request(
    epoint_client: 'EPointClientClass',
    epoint_mock_save_card_failed_response,
    mocker: MockerFixture,
):
    from integrify.epoint.schemas.enums import TransactionStatus

    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_save_card_failed_response,
    ):
        resp = epoint_client.save_card()

        assert not resp.ok
        assert resp.body.status == TransactionStatus.ERROR
        assert resp.body.card_id is None
