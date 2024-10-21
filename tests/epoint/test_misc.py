from httpx import Response
from integrify.epoint.client import EPointClientClass
from integrify.epoint.schemas.parts import TransactionStatus, TransactionStatusExtended
from pytest_mock import MockerFixture

from tests.epoint.mocks import MESSAGE_TRANSACTION_FAIL


def test_ok_signature(
    epoint_client: EPointClientClass,
    epoint_mock_get_transaction_status_success_response: Response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_get_transaction_status_success_response,
    ):
        resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

        assert resp.ok
        assert resp.body.status == TransactionStatusExtended.SUCCESS


def test_wrong_signature(
    epoint_set_wrong_env,
    epoint_client: EPointClientClass,
    epoint_mock_bad_signature_response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_bad_signature_response,
    ):
        resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

        assert not resp.ok
        assert resp.body.status == TransactionStatusExtended.SERVER_ERROR
        assert resp.body.message == 'Signature did not match'


def test_get_failed_transaction_status(
    epoint_client: EPointClientClass,
    epoint_mock_get_transaction_status_failed_response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_get_transaction_status_failed_response,
    ):
        resp = epoint_client.get_transaction_status(transaction_id='texxxxxx')

        assert resp.ok
        assert resp.body.status == TransactionStatusExtended.ERROR
        assert resp.body.message == MESSAGE_TRANSACTION_FAIL


def test_epoint_save_card_request(
    epoint_client: EPointClientClass,
    epoint_mock_save_card_response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_save_card_response,
    ):
        resp = epoint_client.save_card()

        assert resp.ok
        assert resp.body.status == TransactionStatus.SUCCESS
        assert resp.body.card_id


def test_epoint_save_card_failed_request(
    epoint_client: EPointClientClass,
    epoint_mock_save_card_failed_response,
    mocker: MockerFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=epoint_mock_save_card_failed_response,
    ):
        resp = epoint_client.save_card()

        assert not resp.ok
        assert resp.body.status == TransactionStatus.ERROR
        assert resp.body.card_id is None
