from datetime import datetime

import pytest
from httpx import Response
from pytest_mock import MockerFixture


@pytest.fixture(scope='package')
def kapital_mock_create_order_response(package_mocker: MockerFixture):
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
def kapital_mock_get_order_info_invalid_id_response(
    package_mocker: MockerFixture,
):
    return Response(
        status_code=500,
        json={
            'error_code': 'ServiceError',
            'error_description': 'no order found',
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_get_detail_order_info_invalid_id_response(
    package_mocker: MockerFixture,
):
    return Response(
        status_code=500,
        json={
            'error_code': 'ServiceError',
            'error_description': 'no order found',
        },
    )


@pytest.fixture(scope='package')
def kapital_mock_save_card_response(package_mocker: MockerFixture):
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
def kapital_mock_pay_and_save_card_response(package_mocker: MockerFixture):
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
def kapital_mock_refund_response(package_mocker: MockerFixture):
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
def kapital_mock_full_reverse_response(package_mocker: MockerFixture):
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
def kapital_mock_clearing_response(package_mocker: MockerFixture):
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
def kapital_mock_partial_reverse_response(package_mocker: MockerFixture):
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
def kapital_mock_order_with_saved_card_response(package_mocker: MockerFixture):
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
def kapital_mock_link_card_token_response(package_mocker: MockerFixture):
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
