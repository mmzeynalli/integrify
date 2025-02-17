import pytest

from integrify.api import APIClient
from tests.mocks import *  # noqa: F403


def pytest_addoption(parser):
    parser.addoption(
        '--live',
        action='store_true',
        dest='liverun',
        default=False,
        help='enable live tests with tokens provided',
    )


live = pytest.mark.skipif("not config.getoption('liverun')", allow_module_level=True)


@pytest.fixture(scope='package')
def api_client():
    yield APIClient(None, 'base_url')


@pytest.fixture(scope='package')
def dry_api_client():
    yield APIClient(None, 'base_url', dry=True)
