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

    parser.addoption(
        '--github',
        action='store_true',
        dest='githubrun',
        default=False,
        help='enable live tests with tokens provided',
    )


live = pytest.mark.skipif("not config.getoption('liverun')", allow_module_level=True)
"""Tests that need live environment to run"""

github = pytest.mark.skipif("not config.getoption('githubrun')", allow_module_level=True)
"""Tests that can run in Github environment"""


@pytest.fixture(scope='package')
def api_client():
    yield APIClient(None, 'base_url')


@pytest.fixture(scope='package')
def dry_api_client():
    yield APIClient(None, 'base_url', dry=True)
