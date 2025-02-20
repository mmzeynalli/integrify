from functools import partial

import pytest
from pytest_mock import MockerFixture

from tests.conftest import requires_env as _requires_env
from tests.epoint.mocks import *  # noqa: F403

requires_env = partial(_requires_env, 'EPOINT_PUBLIC_KEY', 'EPOINT_PRIVATE_KEY')


@pytest.fixture(scope='function')
def epoint_set_wrong_public_key(mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'epoint.EPOINT_PUBLIC_KEY')
    yield


@pytest.fixture(scope='function')
def epoint_set_wrong_private_key(mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PRIVATE_KEY', 'epoint.EPOINT_PRIVATE_KEY')
    yield


@pytest.fixture(scope='package')
def epoint_client():
    from integrify.epoint.client import EPointClientClass

    yield EPointClientClass()
