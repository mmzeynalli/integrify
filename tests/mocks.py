import pytest
from httpx import Response

from tests.mocks import *  # noqa: F403


@pytest.fixture(scope='package')
def test_response():
    return Response(
        status_code=200,
        json={'data1': 'data1', 'data2': 'data2'},
    )
