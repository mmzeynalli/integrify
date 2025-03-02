from integrify.postaguvercini.client import PostaGuverciniClientClass
from integrify.postaguvercini.schemas.enums import StatusCode
from tests.postaguvercini.conftest import requires_env


def test_wrong_login(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.credit_balance(
        username='wrong_username', password='wrong_password'
    )
    assert resp.body.status_code == 500
    assert resp.body.status_description == 'Daxilolma məlumatlarında xəta var!'
    assert resp.body.result is None


@requires_env()
def test_empty_receiver_list(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.send_single_sms(message='test', receivers=[])

    assert resp.status_code == 500
    assert resp.body.status_code == StatusCode.EMPTY_RECEIVER_LIST
    assert resp.body.status_description == 'Receivers cannot be empty. (ERR1060)'


@requires_env()
def test_empty_msg(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.send_single_sms(message='', receivers=['99450'])

    assert resp.status_code == 500
    assert resp.body.status_code == StatusCode.MESSAGE_EMPTY
    assert resp.body.status_description == 'Messages is cannot be empty. (ERR1090)'


@requires_env()
def test_max_recipient(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.send_multiple_sms(
        messages=[{'receiver': '99450', 'message': 'test'}] * 1000,
    )

    assert resp.status_code == 500
    assert resp.body.status_code == StatusCode.MAX_NUMBER_OF_RECIPIENTS
    assert (
        resp.body.status_description == 'Your request could not be recorded. You must add no more '
        'than 800 recipients at once. (ERR1070)'
    )


@requires_env()
def test_wrong_send_date_format(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.send_single_sms(message='test', receivers=['99450'], send_date='1')

    assert resp.status_code == 500
    assert resp.body.status_code == StatusCode.INVALID_SEND_DATE_FORMAT
    assert (
        resp.body.status_description == 'SendDate: Must be in the format yyyyMMdd HH:mm. (ERR1063)'
    )


@requires_env()
def test_wrong_expiry_date_format(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.send_single_sms(
        message='test', receivers=['99450'], expire_date='1'
    )

    assert resp.status_code == 500
    assert resp.body.status_code == StatusCode.INVALID_EXPIRE_DATE_FORMAT
    assert (
        resp.body.status_description == 'ExpireDate: Must be in the format yyyyMMdd HH:mm. (1064)'
    )


@requires_env()
def test_non_existent_transaction(postaguvercini_client: PostaGuverciniClientClass):
    resp = postaguvercini_client.get_status(message_ids=['randomid'])

    assert resp.status_code == 200
    assert resp.body.result[0].sms_status == ''
    assert resp.body.result[0].sms_status_description == 'Bilinmiyor ?'
