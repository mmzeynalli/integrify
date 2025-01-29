import pytest

from integrify.azericard.client import AzeriCardClientClass


@pytest.fixture(scope='package')
def epoint_client():
    yield AzeriCardClientClass()
