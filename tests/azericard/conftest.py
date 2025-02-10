import io
import os

import pytest
from pytest_mock import MockerFixture

from .mocks import *  # noqa: F403


@pytest.fixture(scope='package')
def azericard_set_env():
    os.environ['AZERICARD_MERCHANT_ID'] = '12345678'
    os.environ['AZERICARD_MERCHANT_NAME'] = 'merchant_name'
    os.environ['AZERICARD_KEY_FILE_PATH'] = 'key_file_path'
    os.environ['AZERICARD_MERCHANT_URL'] = 'merchant.url'
    os.environ['AZERICARD_MERCHANT_EMAIL'] = 'merchant@email.com'
    os.environ['AZERICARD_CALLBACK_URL'] = 'callback.url'

    yield


@pytest.fixture(scope='function', autouse=True)
def mock_private_key_file_reading(mocker: MockerFixture):
    with mocker.patch(
        'builtins.open',
        return_value=io.StringIO('test_private_key'),
    ):
        yield


@pytest.fixture(scope='package')
def azericard_client(azericard_set_env):
    from integrify.azericard.client import AzeriCardClientClass

    yield AzeriCardClientClass()
