import pytest

from integrify.lsim.client import LSIMClientClass


@pytest.fixture(scope='package')
def lsim_client():
    yield LSIMClientClass()
