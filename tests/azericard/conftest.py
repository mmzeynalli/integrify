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
def mock_private_key_file_reading(request: pytest.FixtureRequest, mocker: MockerFixture):
    # Random Private Key, generated from
    key = """-----BEGIN RSA PRIVATE KEY-----
            MIIBOQIBAAJAc/aeBVL37Jvd5fZBjM/ENRsVa0TnqcGbmx0K1RCzoOg4g2wIK/Fy
            PV7Dm+vLuunrueh7vXzTlxZdAteUN8+rrwIDAQABAkBC8dpj5HPwCkNd4H4TFlaE
            +e+xj4PVwklckLWSLyQj/V9yOzebCHwIoRMF08yTOxvzJoS4RjMHbom2IGZZEPGB
            AiEA2P/0U9DOpnoC7OjpJIJBSfgJ04M8H4BzeNC3Uw/nGCECIQCIzgdiJH1nhKPn
            N3o2ePt1SWk/V81axkEfaS06sNoJzwIhAIrEs8RdxakkYXaLQ3y7Z3EcE3yVcf9b
            L3zVTEbr5obBAiAkI9FdguhCDY9DCKvXchRzwoX0Pty4C0Gu65kQNSIUjwIgLc5j
            gdx2NeK8j3Dye22xqPT5lvPOC+O/LNZ7lmrAybw=
            -----END RSA PRIVATE KEY-----"""

    if 'key_as_string' in request.keywords:
        klass = io.StringIO
    else:
        klass = io.BytesIO
        key = key.encode()

    with mocker.patch('builtins.open', return_value=klass(key)):
        yield


@pytest.fixture(scope='package')
def azericard_client(azericard_set_env):
    from integrify.azericard.client import AzeriCardClientClass

    yield AzeriCardClientClass()
