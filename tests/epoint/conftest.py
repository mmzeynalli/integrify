import base64
import json
from hashlib import sha1
from typing import Any

import pytest
from integrify.base import ApiResponse
from integrify.epoint.schemas.parts import TransactionStatus
from integrify.epoint.sync import EPointRequestClass
from pytest_mock import MockerFixture

from tests import epoint
from tests.epoint.mocks import *  # noqa: F403


class TestEPointRequest(EPointRequestClass):
    __test__ = False

    def __init__(self, resp_data: dict):
        super().__init__()
        self.resp_data = resp_data


@pytest.fixture(autouse=True, scope='package')
def epoint_request_mocker(package_mocker: MockerFixture):
    package_mocker.patch('integrify.base.SyncApiRequest.__call__', new=req)
    yield


@pytest.fixture(autouse=True, scope='package')
def epoint_setenv(package_mocker: MockerFixture):
    package_mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', epoint.EPOINT_PUBLIC_KEY)
    package_mocker.patch('integrify.epoint.env.EPOINT_PRIVATE_KEY', epoint.EPOINT_PRIVATE_KEY)
    yield


@pytest.fixture(scope='function')
def epoint_set_wrong_env(mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'epoint.EPOINT_PUBLIC_KEY')
    mocker.patch('integrify.epoint.env.EPOINT_PRIVATE_KEY', 'epoint.EPOINT_PRIVATE_KEY')
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


def req(self: TestEPointRequest, *args, **kwds):
    resp: dict[str, Any]

    if not is_signature_ok(self.body):
        resp = {
            'body': {
                'status': TransactionStatus.SERVER_ERROR,
                'message': 'Signature did not match',
            }
        }
    else:
        resp = self.resp_data.copy()

    if not resp:
        raise Exception('Mock response data should be provided')

    resp.setdefault('is_success', True)
    resp.setdefault('status_code', 200)
    resp.setdefault('headers', {})

    return ApiResponse[self.resp_model].model_validate(resp)  # type: ignore[name-defined]
