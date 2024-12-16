import os

import pytest

from integrify.kapital.client import KapitalClientClass
from tests import kapital
from tests.kapital.mocks import *  # noqa: F403


@pytest.fixture(autouse=True, scope='session')
def kapital_setenv():
    os.environ['KAPITAL_ENV'] = kapital.KAPITAL_ENV
    os.environ['KAPITAL_USERNAME'] = kapital.KAPITAL_USERNAME
    os.environ['KAPITAL_PASSWORD'] = kapital.KAPITAL_PASSWORD

    yield


@pytest.fixture(scope='session')
def kapital_set_wrong_env():
    os.environ['KAPITAL_ENV'] = 'test'
    os.environ['KAPITAL_USERNAME'] = 'TerminalSys/notkapital'
    os.environ['KAPITAL_PASSWORD'] = 'notkapital123'

    yield


@pytest.fixture(scope='module')
def kapital_order(kapital_client: KapitalClientClass):
    """
    Fixture to manage shared state for order creation and retrieval.
    """
    create_response = kapital_client.create_order(
        amount=1,
        currency='AZN',
        description='test',
    )

    assert create_response.body.data is not None, 'Response data is None'

    assert create_response.status_code == 200
    assert create_response.body.data.redirect_url.startswith('https://txpgtst.kapitalbank.az')

    yield create_response.body.data


@pytest.fixture(scope='package')
def kapital_client():
    yield KapitalClientClass()
