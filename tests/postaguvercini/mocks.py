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
