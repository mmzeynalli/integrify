import pytest
from httpx import Response
from integrify.epoint.schemas.parts import TransactionStatus, TransactionStatusExtended
from pytest_mock import MockerFixture

MESSAGE_SUCCESS = 'Təsdiq edildi'
MESSAGE_SERVER_ERROR = 'Signature did not match'
MESSAGE_TRANSACTION_FAIL = 'Kartda kifayət qədər balans yoxdur'


@pytest.fixture(scope='package')
def epoint_mock_get_transaction_status_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.SUCCESS,
            'message': MESSAGE_SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
            'code': '',
            'order_id': 'random_order_id',
            'other_attr': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_get_transaction_status_failed_response():
    # Request is successful, transaction was not
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.ERROR,
            'message': MESSAGE_TRANSACTION_FAIL,
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
            'code': '',
            'order_id': 'random_order_id',
            'other_attr': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_bad_signature_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.SERVER_ERROR,
            'message': MESSAGE_SERVER_ERROR,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'redirect_url': 'https://epoint.az',
            'card_id': 'cexxxxxxxxxx',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_save_card_failed_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.ERROR,
            'redirect_url': None,
            'card_id': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_payment_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_pay_and_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_pay_with_saved_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_payout_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_refund_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.SUCCESS, 'message': 'Approved'},
    )


@pytest.fixture(scope='package')
def epoint_mock_split_payment_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_split_pay_with_saved_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 100,
            'split_amount': 50,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_split_pay_and_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        },
    )
