import os

from integrify.lsim.bulk.client import LSIMBulkSMSClientClass
from integrify.lsim.bulk.schemas.enums import Code
from tests.conftest import live
from tests.lsim.conftest import requires_env


@requires_env()
def test_invalid_task_id(lsim_bulksms_client: LSIMBulkSMSClientClass):
    assert (
        lsim_bulksms_client.get_detailed_report_with_dates(taskid='0').body.response_code
        == Code.INVALID_AUTH
    )


@requires_env('PHONE_NUMBER_1')
def test_duplicate_controlid(lsim_bulksms_client: LSIMBulkSMSClientClass):
    assert (
        lsim_bulksms_client.bulk_send_one_message(
            controlid='1', msisdns=[os.getenv('PHONE_NUMBER_1')], bulkmessage='Test Message!'
        ).body.response_code
        == Code.DUPLICATE
    )


@requires_env('PHONE_NUMBER_1')
@live
def test_invalid_login(lsim_bulksms_client: LSIMBulkSMSClientClass):
    assert (
        lsim_bulksms_client.bulk_send_one_message(
            controlid='1',
            msisdns=[os.getenv('PHONE_NUMBER_1')],
            bulkmessage='Test Message!',
            login='login',
        ).body.response_code
        == Code.INVALID_AUTH
    )


@requires_env('PHONE_NUMBER_1')
@live
def test_invalid_pass(lsim_bulksms_client: LSIMBulkSMSClientClass):
    assert (
        lsim_bulksms_client.bulk_send_one_message(
            controlid='1',
            msisdns=[os.getenv('PHONE_NUMBER_1')],
            bulkmessage='Test Message!',
            password='password',
        ).body.response_code
        == Code.INVALID_AUTH
    )
