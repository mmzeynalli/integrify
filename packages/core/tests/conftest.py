import pytest

from integrify.api import APIClient
from tests.mocks import *  # noqa: F403


@pytest.fixture(scope='package')
def api_client():
    yield APIClient(None, 'base_url')


@pytest.fixture(scope='package')
def dry_api_client():
    yield APIClient(None, 'base_url', dry=True)
