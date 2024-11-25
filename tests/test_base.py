from unittest.mock import patch

import pytest
from httpx import Response
from pydantic import BaseModel
from pytest_mock import MockerFixture

from integrify.api import APIClient, APIPayloadHandler
from integrify.schemas import PayloadBaseModel


class RequestSchema(PayloadBaseModel):
    data1: str


class ResponseSchema(BaseModel):
    data1: str
    data2: str


def test_unimplemented_function(api_client: APIClient):
    with pytest.raises(AttributeError):
        api_client.login()


def test_no_handler(api_client: APIClient, test_ok_response, mocker: MockerFixture):
    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        resp = api_client.test()
        assert isinstance(resp, Response)
        assert resp.json()['data1'] == 'data1'
        assert resp.json()['data2'] == 'data2'


def test_missing_request_handler_noinput(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(None, ResponseSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        resp = api_client.test()
        api_client.add_handler('test', Handler)
        assert isinstance(resp, Response)
        assert resp.json()['data1'] == 'data1'
        assert resp.json()['data2'] == 'data2'


def test_missing_request_handler_input(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(None, ResponseSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        # Should not give exception
        api_client.test(data1='data1')
        # Should give an exception
        with pytest.raises(AssertionError):
            api_client.test('data1')


def test_missing_response_handler_input(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(RequestSchema, None)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='data1')
        assert isinstance(resp.body, dict)
        assert resp.body['data1'] == 'data1'
        assert resp.body['data2'] == 'data2'


def test_with_handlers(api_client: APIClient, test_ok_response, mocker: MockerFixture):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(RequestSchema, ResponseSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='data1')
        assert isinstance(resp.body, ResponseSchema)
        assert resp.body.data1 == 'data1'
        assert resp.body.data2 == 'data2'


def test_error_log(test_error_response, mocker: MockerFixture):
    with mocker.patch('httpx.Client.request', return_value=test_error_response):
        from integrify.api import APIClient

        api_client = APIClient('')
        with patch.object(api_client.request_executor.logger, 'error') as mock:
            api_client.add_url('test', 'url', 'GET', 'base_url')
            resp = api_client.test(data1='data1')

            assert mock.call_count
            assert not resp.is_success
