import base64
import json
from hashlib import sha1

import pytest
from pytest_mock import MockerFixture

from integrify.base import ApiResponse, SyncApiRequest
from integrify.epoint.schemas.parts import EPointTransactionStatus
from tests import epoint
from tests.epoint.mocks import *  # noqa: F403


@pytest.fixture(autouse=True, scope='package')
def epoint_request_mocker(package_mocker: MockerFixture):
    package_mocker.patch('integrify.base.SyncApiRequest.__call__', new=req)
    yield


@pytest.fixture(autouse=True, scope='package')
def epoint_setenv(package_mocker: MockerFixture):
    package_mocker.patch('integrify.epoint.EPOINT_PUBLIC_KEY', epoint.EPOINT_PUBLIC_KEY)
    package_mocker.patch('integrify.epoint.EPOINT_PRIVATE_KEY', epoint.EPOINT_PRIVATE_KEY)
    yield


@pytest.fixture(scope='function')
def epoint_set_wrong_env(mocker: MockerFixture):
    mocker.patch('integrify.epoint.EPOINT_PUBLIC_KEY', 'epoint.EPOINT_PUBLIC_KEY')
    mocker.patch('integrify.epoint.EPOINT_PRIVATE_KEY', 'epoint.EPOINT_PRIVATE_KEY')
    yield


def epoint_mock_generate_signature(data: str):
    sgn_string = epoint.EPOINT_PRIVATE_KEY + data + epoint.EPOINT_PRIVATE_KEY
    return base64.b64encode(sha1(sgn_string.encode()).digest()).decode()


def is_signature_ok(data: dict):
    if data['signature'] != epoint_mock_generate_signature(data['data']):
        return False

    return (
        json.loads(base64.b64decode(data['data']).decode())['public_key']
        == epoint.EPOINT_PUBLIC_KEY
    )


def req(req_cls: SyncApiRequest, data: dict):
    resp = (
        {
            'body': {
                'status': EPointTransactionStatus.SERVER_ERROR,
                'message': 'Signature did not match',
            }
        }
        if not is_signature_ok(req_cls.body)
        else data
    )

    if not resp:
        raise Exception('Mock response data should be provided')

    resp.setdefault('is_success', True)
    resp.setdefault('status_code', 200)
    resp.setdefault('headers', {})
    return ApiResponse[req_cls.resp_model].model_validate(resp)  # type: ignore[name-defined]
