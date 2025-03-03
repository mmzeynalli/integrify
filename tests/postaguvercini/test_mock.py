from httpx import Response
from pytest_mock import MockFixture

from integrify.postaguvercini.client import PostaGuverciniClientClass
from tests.postaguvercini.conftest import requires_env


@requires_env()
def test_mock_single_sms_request(
    postaguvercini_client: PostaGuverciniClientClass,
    postaguvercini_mock_single_sms_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=postaguvercini_mock_single_sms_response,
    ):
        resp = postaguvercini_client.send_single_sms(message='test', receivers=['994123456789'])

        assert resp.body.status_code == 200
        assert resp.body.status_description == 'Test'
        assert resp.body.result[0].message_id == '1234'
        assert resp.body.result[0].receiver == '994123456789'
        assert resp.body.result[0].charge == 1


@requires_env()
def test_mock_multiple_sms_request(
    postaguvercini_client: PostaGuverciniClientClass,
    postaguvercini_mock_multiple_sms_response: Response,
    mocker: MockFixture,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=postaguvercini_mock_multiple_sms_response,
    ):
        resp = postaguvercini_client.send_multiple_sms(
            messages=[
                {'receiver': '994123456789', 'message': 'Test SMS 1'},
                {'receiver': '994123456780', 'message': 'Test SMS 2'},
            ]
        )

        assert resp.body.status_code == 200
        assert resp.body.result[0].message_id == '1234'
        assert resp.body.result[0].receiver == '994123456789'
        assert resp.body.result[1].receiver == '994123456780'
