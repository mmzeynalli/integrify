import pytest
from httpx import Response


@pytest.fixture(scope='package')
def postaguvercini_mock_single_sms_response():
    return Response(
        status_code=200,
        json={
            'status_code': 200,
            'status_description': 'Test',
            'result': [
                {
                    'message_id': '1234',
                    'receiver': '994123456789',
                    'charge': 1,
                }
            ],
        },
    )


@pytest.fixture(scope='package')
def postaguvercini_mock_multiple_sms_response():
    return Response(
        status_code=200,
        json={
            'status_code': 200,
            'status_description': 'Test',
            'result': [
                {
                    'message_id': '1234',
                    'receiver': '994123456789',
                    'charge': 1,
                },
                {
                    'message_id': '1235',
                    'receiver': '994123456780',
                    'charge': 1,
                },
            ],
        },
    )


@pytest.fixture(scope='package')
def postaguvercini_mock_status_response():
    return Response(
        status_code=200,
        json={
            'status_code': 200,
            'status_description': 'Test',
            'result': [
                {
                    'message_id': '1234',
                    'receiver': '994123456789',
                    'sms_status': '400',
                    'sms_status_description': 'Çatdı',
                    'is_final_status': '1',
                    'status_time': '20250220 12:14',
                    'sms_charge': '1',
                }
            ],
        },
    )


@pytest.fixture(scope='package')
def postaguvercini_mock_credit_balance_response():
    return Response(
        status_code=200,
        json={
            'status_code': 200,
            'status_description': 'Test',
            'result': {'balance': 30},
        },
    )
