import os

from integrify.lsim.single.client import LSIMSingleSMSClientClass
from integrify.lsim.single.schemas.enums import Code
from tests.conftest import live
from tests.lsim.conftest import requires_env


@requires_env()
def test_invalid_trans_id(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.get_report_get(trans_id=0).body.error_code
        == Code.INVALID_TRANSACTION_ID
    )


@requires_env('LSIM_SENDER_NAME')
def test_wrong_number_format(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.send_sms_get(msisdn='99455555555', text='test').body.error_code
        == Code.WRONG_NUMBER_FORMAT
    )


@requires_env('LSIM_SENDER_NAME', 'PHONE_NUMBER_1')
def test_too_long_text(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.send_sms_post(
            msisdn=os.getenv('PHONE_NUMBER_1'), text='test' * 251
        ).body.error_code
        == Code.INTERNAL_ERROR._name_
    )


@requires_env('PHONE_NUMBER_1')
@live
def test_invalid_login(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.send_sms_get(
            msisdn=os.getenv('PHONE_NUMBER_1'),
            text='test',
            login='invalid',
        ).body.error_code
        == Code.INVALID_KEY
    )


@requires_env('PHONE_NUMBER_1')
@live
def test_invalid_pass(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.send_sms_get(
            msisdn=os.getenv('PHONE_NUMBER_1'),
            text='test',
            password='invalid',
        ).body.error_code
        == Code.INVALID_HASH
    )


@requires_env('PHONE_NUMBER_1')
@live
def test_invalid_sender(lsim_singlesms_client: LSIMSingleSMSClientClass):
    assert (
        lsim_singlesms_client.send_sms_get(
            msisdn=os.getenv('PHONE_NUMBER_1'),
            text='test',
            sender='invalid',
        ).body.error_code
        == Code.INVALID_SENDER_NAME
    )
