from functools import partial

import pytest

from integrify.lsim.bulk.client import LSIMBulkSMSClientClass
from integrify.lsim.single.client import LSIMSingleSMSClientClass
from tests.conftest import requires_env as _requires_env

requires_env = partial(_requires_env, 'LSIM_LOGIN', 'LSIM_PASSWORD')


@pytest.fixture(scope='package')
def lsim_singlesms_client():
    yield LSIMSingleSMSClientClass()


@pytest.fixture(scope='package')
def lsim_bulksms_client():
    yield LSIMBulkSMSClientClass()
