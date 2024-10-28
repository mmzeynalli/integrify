import pytest
from integrify.epoint.client import EPointClientClass
from pytest_mock import MockerFixture

from tests import epoint
from tests.epoint.mocks import *  # noqa: F403


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


@pytest.fixture(scope='package')
def epoint_client():
    yield EPointClientClass()
