from functools import partial

import pytest

from integrify.lsim.client import LSIMClientClass
from tests.conftest import requires_env as _requires_env

requires_env = partial(_requires_env, 'LSIM_LOGIN', 'LSIM_PASSWORD')


@pytest.fixture(scope='package')
def lsim_client():
    yield LSIMClientClass()
