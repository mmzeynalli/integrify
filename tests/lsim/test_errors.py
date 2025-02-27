from integrify.lsim.client import LSIMClientClass
from integrify.lsim.schemas.enums import Code
from tests.lsim.conftest import requires_env


@requires_env()
def test_invalid_trans_id(lsim_client: LSIMClientClass):
    assert lsim_client.get_report_get(trans_id=0).body.error_code == Code.INVALID_TRANSACTION_ID


@requires_env('LSIM_SENDER_NAME')
def test_wrong_number_format(lsim_client: LSIMClientClass):
    assert (
        lsim_client.send_sms_get(msisdn='99455555555', text='test').body.error_code
        == Code.WRONG_NUMBER_FORMAT
    )


@requires_env('LSIM_SENDER_NAME')
def test_too_long_text(lsim_client: LSIMClientClass):
    assert (
        lsim_client.send_sms_post(msisdn='994555779018', text='test' * 251).body.error_code
        == Code.INTERNAL_ERROR._name_
    )


@requires_env()
def test_invalid_login(lsim_client: LSIMClientClass):
    assert (
        lsim_client.send_sms_get(
            msisdn='994555779018',
            text='test',
            login='invalid',
        ).body.error_code
        == Code.INVALID_KEY
    )


@requires_env()
def test_invalid_pass(lsim_client: LSIMClientClass):
    from integrify.lsim.schemas.enums import Code

    assert (
        lsim_client.send_sms_get(
            msisdn='994555779018',
            text='test',
            password='invalid',
        ).body.error_code
        == Code.INVALID_HASH
    )


@requires_env('LSIM_SENDER_NAME')
def test_invalid_sender(lsim_client: LSIMClientClass):
    from integrify.lsim.schemas.enums import Code

    assert (
        lsim_client.send_sms_get(
            msisdn='994555779018',
            text='test',
            sender='invalid',
        ).body.error_code
        == Code.INVALID_SENDER_NAME
    )
