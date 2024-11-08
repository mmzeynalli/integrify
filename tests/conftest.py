import pytest

from integrify.api import APIClient
from tests.mocks import *  # noqa: F403


@pytest.fixture(scope='package')
def api_client():
    yield APIClient(None, 'base_url')
