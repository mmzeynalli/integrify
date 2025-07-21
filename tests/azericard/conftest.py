from functools import partial

import pytest

from tests.conftest import requires_env as _requires_env

from .mocks import *  # noqa: F403

requires_env = partial(
    _requires_env,
    'AZERICARD_MERCHANT_ID',
    'AZERICARD_MERCHANT_NAME',
    'AZERICARD_KEY_FILE_PATH',
    'AZERICARD_MERCHANT_URL',
    'AZERICARD_MERCHANT_EMAIL',
    'AZERICARD_CALLBACK_URL',
)


@pytest.fixture(scope='package')
def azericard_client():
    from integrify.azericard.client import AzeriCardClientClass

    yield AzeriCardClientClass()
