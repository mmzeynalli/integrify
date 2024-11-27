import pytest
from httpx import Response

from tests.mocks import *  # noqa: F403


@pytest.fixture(scope='package')
def test_ok_response():
    return Response(
        status_code=200,
        json={'data1': 'output1', 'data2': 'output2'},
    )


@pytest.fixture(scope='package')
def test_error_response():
    return Response(
        status_code=404,
        json={'data1': 'NotFound', 'data2': 'NotFound'},
    )
