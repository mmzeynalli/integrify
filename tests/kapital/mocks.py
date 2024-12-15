from datetime import datetime

import pytest
from httpx import Response
from pytest_mock import MockerFixture


@pytest.fixture(scope='package')
def kapital_mock_refund_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'tran': {
                'approvalCode': 'refund_123',
                'pmoResultCode': '1000',
                'match': {
                    'tranActionId': '123',
                    'ridByPmo': '123',
                },
            }
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_full_reverse_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'tran': {
                'pmoResultCode': '1000',
                'match': {
                    'tranActionId': '123',
                    'ridByPmo': '123',
                },
            }
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_clearing_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'tran': {
                'pmoResultCode': '1000',
                'match': {
                    'tranActionId': '123',
                    'ridByPmo': '123',
                },
            }
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_partial_reverse_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'tran': {
                'pmoResultCode': '1000',
                'match': {
                    'tranActionId': '123',
                    'ridByPmo': '123',
                },
            }
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_order_with_saved_card_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'order': {
                'id': 1231,
                'password': '1231231',
                'hpp_url': 'https://txpgtst.kapitalbank.az',
            }
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_link_card_token_success_response(package_mocker: MockerFixture):
    return Response(
        status_code=200,
        json={
            'order': {
                'status': 'PreAuth',
                'cvv2_auth_status': 'test',
                'tds_v1_auth_status': 'test',
                'tds_v2_auth_status': 'test',
                'otp_aut_status': 'test',
                'src_token': {
                    'id': 1,
                    'payment_method': 'test',
                    'role': 'test',
                    'status': 'test',
                    'reg_time': datetime.now().isoformat(),
                    'entry_mode': 'test',
                    'display_name': 'test',
                    'card': {
                        'expiration': 'test',
                        'brand': 'test',
                        'issuer_rid': 'test',
                    },
                },
            }
        },
    )
