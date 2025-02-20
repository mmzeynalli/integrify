import os

import pytest

from integrify.postaguvercini.client import PostaGuverciniClientClass
from tests import postaguvercini
from tests.postaguvercini.mocks import *  # noqa: F403


@pytest.fixture(autouse=True, scope='session')
def postaguvercini_setenv():
    os.environ['POSTA_GUVERCINI_USERNAME'] = postaguvercini.POSTA_GUVERCINI_USERNAME
    os.environ['POSTA_GUVERCINI_PASSWORD'] = postaguvercini.POSTA_GUVERCINI_PASSWORD

    yield


@pytest.fixture(scope='session')
def postaguvercini_set_wrong_env():
    os.environ['POSTA_GUVERCINI_USERNAME'] = 'test'
    os.environ['POSTA_GUVERCINI_PASSWORD'] = 'test'

    yield


@pytest.fixture(scope='package')
def postaguvercini_client():
    yield PostaGuverciniClientClass()
