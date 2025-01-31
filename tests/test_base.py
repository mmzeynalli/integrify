from unittest.mock import patch

import httpx
import pytest
from httpx import Response
from pydantic import BaseModel
from pytest_mock import MockerFixture

from integrify.api import APIClient, APIPayloadHandler
from integrify.schemas import PayloadBaseModel


class RequestSchema(PayloadBaseModel):
    data1: str


class RequestWithURLParamSchema(RequestSchema):
    URL_PARAM_FIELDS = {'data1'}


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
        assert resp.json()['data1'] == 'output1'
        assert resp.json()['data2'] == 'output2'


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
        assert resp.json()['data1'] == 'output1'
        assert resp.json()['data2'] == 'output2'


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
        api_client.test(data1='input1')
        # Should give an exception
        with pytest.raises(AssertionError):
            api_client.test('data1')


def test_default_response_handler_input(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(req_model=RequestSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='input1')
        assert isinstance(resp.body, dict)
        assert resp.body['data1'] == 'output1'
        assert resp.body['data2'] == 'output2'


def test_none_response_handler_input(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(req_model=RequestSchema, resp_model=None)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='input1')
        assert isinstance(resp, httpx.Response)
        assert resp.json()['data1'] == 'output1'
        assert resp.json()['data2'] == 'output2'


def test_with_handlers(api_client: APIClient, test_ok_response, mocker: MockerFixture):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(RequestSchema, ResponseSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='input1')
        assert isinstance(resp.body, ResponseSchema)
        assert resp.body.data1 == 'output1'
        assert resp.body.data2 == 'output2'


def test_error_log(test_error_response, mocker: MockerFixture):
    with mocker.patch('httpx.Client.request', return_value=test_error_response):
        from integrify.api import APIClient

        api_client = APIClient('')
        with patch.object(api_client.request_executor.logger, 'error') as mock:
            api_client.add_url('test', 'url', 'GET', 'base_url')
            resp = api_client.test(data1='input1')

            assert mock.call_count
            assert not resp.is_success


def test_url_formatting_ok(api_client: APIClient, test_ok_response, mocker: MockerFixture):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(RequestWithURLParamSchema, ResponseSchema)

    with mocker.patch('httpx.Client.request', return_value=test_ok_response):
        api_client.add_url('test', 'url?q={data1}', 'GET')
        api_client.add_handler('test', Handler)
        resp = api_client.test(data1='input1')
        assert isinstance(resp.body, ResponseSchema)
        assert resp.body.data1 == 'output1'
        assert resp.body.data2 == 'output2'


@pytest.mark.parametrize('req_schema', (RequestSchema, None))
def test_url_formatting_fail_without_url_params(
    api_client: APIClient,
    test_ok_response,
    mocker: MockerFixture,
    req_schema,
):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(req_schema, ResponseSchema)

    with (
        mocker.patch('httpx.Client.request', return_value=test_ok_response),
        pytest.raises(ValueError),
    ):
        api_client.add_url('test', 'url?q={data1}', 'GET')
        api_client.add_handler('test', Handler)
        api_client.test(data1='input1')  # raises ValueError


def test_dry_run_none(dry_api_client):
    dry_api_client.add_url('test', 'url', 'GET')
    resp = dry_api_client.test()
    assert isinstance(resp.body, dict)
    assert 'url' in resp.body


def test_dry_run_json(dry_api_client):
    class Handler(APIPayloadHandler):
        def __init__(self):
            super().__init__(RequestSchema, ResponseSchema)

    dry_api_client.add_url('test', 'url', 'GET')
    dry_api_client.add_handler('test', Handler)
    resp = dry_api_client.test(data1='input1')
    assert isinstance(resp.body, dict)
    assert resp.body['data']['data1'] == 'input1'
