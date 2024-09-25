from decimal import Decimal

import pytest

from integrify.epoint.schemas.parts import TransactionStatus, TransactionStatusExtended

MESSAGE_SUCCESS = 'Təsdiq edildi'
MESSAGE_SERVER_ERROR = 'Signature did not match'


@pytest.fixture(scope='package')
def epoint_mock_get_transaction_status_response():
    return {
        'body': {
            'status': TransactionStatusExtended.SUCCESS,
            'message': MESSAGE_SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': Decimal(1),
            'code': '',
            'order_id': 'random_order_id',
            'other_attr': None,
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_save_card_response():
    return {
        'body': {
            'status': 'success',
            'redirect_url': 'https://epoint.az',
            'card_id': 'cexxxxxxxxxx',
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_payment_response():
    return {
        'body': {
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_pay_and_save_card_response():
    return {
        'body': {
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_pay_with_saved_card_response():
    return {
        'body': {
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
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_split_payment_response():
    return {
        'body': {
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_split_pay_with_saved_card_response():
    return {
        'body': {
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
        }
    }


@pytest.fixture(scope='package')
def epoint_mock_split_pay_and_save_card_response():
    return {
        'body': {
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        }
    }