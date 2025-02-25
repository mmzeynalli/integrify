import os

from integrify.postaguvercini.client import PostaGuverciniClientClass
from tests.conftest import live
from tests.postaguvercini.conftest import requires_env


@requires_env('POSTAGUVERCINI_RECEIVER')
@live
def test_single_sms_request(postaguvercini_client: PostaGuverciniClientClass):
    old_balance = postaguvercini_client.credit_balance().body.result.balance

    postaguvercini_client.send_single_sms(
        message='test', receivers=[os.getenv('POSTAGUVERCINI_RECEIVER')]
    )

    new_balance = postaguvercini_client.credit_balance().body.result.balance

    assert new_balance + 1 == old_balance


@requires_env('POSTAGUVERCINI_RECEIVER')
@live
def test_multiple_sms_request(
    postaguvercini_client: PostaGuverciniClientClass,
):
    old_balance = postaguvercini_client.credit_balance().body.result.balance

    postaguvercini_client.send_multiple_sms(
        messages=[
            {'receiver': os.getenv('POSTAGUVERCINI_RECEIVER'), 'message': 'Test SMS 1'},
            {'receiver': os.getenv('POSTAGUVERCINI_RECEIVER'), 'message': 'Test SMS 2'},
        ]
    )

    new_balance = postaguvercini_client.credit_balance().body.result.balance

    assert new_balance + 2 == old_balance


@requires_env('POSTAGUVERCINI_MESSAGE_ID')
def test_status_request(
    postaguvercini_client: PostaGuverciniClientClass,
):
    message_id = os.getenv('POSTAGUVERCINI_MESSAGE_ID')
    resp = postaguvercini_client.status(message_ids=[message_id])

    assert resp.status_code == 200
    assert resp.body.status_code == 200
    assert resp.body.result[0].message_id == message_id
    assert resp.body.result[0].sms_status_description == 'Çatdı'


@requires_env()
def test_credit_balance_request(
    postaguvercini_client: PostaGuverciniClientClass,
):
    resp = postaguvercini_client.credit_balance()

    assert resp.body.status_code == 200
    assert resp.body.status_description == 'Transaction done successfully'
