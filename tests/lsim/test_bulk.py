import os

from integrify.lsim.bulk.client import LSIMBulkSMSClientClass
from integrify.lsim.bulk.schemas.enums import Code, SMSStatus
from tests.conftest import live
from tests.lsim.conftest import requires_env


@live
@requires_env('PHONE_NUMBER_1', 'PHONE_NUMBER_2')
def test_send_one_bulk_message(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    assert (
        lsim_bulksms_client.bulk_send_one_message(
            controlid='1',
            msisdns=[os.getenv('PHONE_NUMBER_1'), os.getenv('PHONE_NUMBER_2')],
            bulkmessage='Test Message!',
        ).body.response_code
        == Code.SUCCESS
    )


@live
@requires_env('PHONE_NUMBER_1', 'PHONE_NUMBER_2')
def test_send_different_bulk_messages(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    assert (
        lsim_bulksms_client.bulk_send_different_messages(
            controlid='2',
            msisdns=[os.getenv('PHONE_NUMBER_1'), os.getenv('PHONE_NUMBER_2')],
            messages=['Test Message 1', 'Test Message 2'],
        ).body.response_code
        == Code.SUCCESS
    )


@requires_env('LSIM_BULK_TRANS_ID')
def test_get_bulk_report(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    resp = lsim_bulksms_client.get_report(taskid=os.getenv('LSIM_BULK_TRANS_ID')).body
    assert resp.response_code == Code.SUCCESS
    assert resp.delivered == 2


@requires_env('LSIM_BULK_TRANS_ID', 'PHONE_NUMBER_1', 'PHONE_NUMBER_2')
def test_get_bulk_detailed_report(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    resp = lsim_bulksms_client.get_detailed_report(taskid=os.getenv('LSIM_BULK_TRANS_ID')).body
    assert resp.response_code == Code.SUCCESS

    for report, number in zip(
        resp.body, [os.getenv('PHONE_NUMBER_2'), os.getenv('PHONE_NUMBER_1')]
    ):
        assert report.date is None  # no date in detailed report
        assert str(report.msisdn) == number
        assert report.status == SMSStatus.MESSAGE_DELIVERED
        assert 'Test Message' in report.message


@requires_env('LSIM_BULK_TRANS_ID', 'PHONE_NUMBER_1', 'PHONE_NUMBER_2')
def test_get_bulk_detailed_with_dates_report(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    resp = lsim_bulksms_client.get_detailed_report_with_dates(
        taskid=os.getenv('LSIM_BULK_TRANS_ID')
    ).body
    assert resp.response_code == Code.SUCCESS

    for report, number in zip(
        resp.body, [os.getenv('PHONE_NUMBER_2'), os.getenv('PHONE_NUMBER_1')]
    ):
        assert report.date is not None  # no date in detailed report
        assert str(report.msisdn) == number
        assert report.status == SMSStatus.MESSAGE_DELIVERED
        assert 'Test Message' in report.message


@requires_env()
def test_check_balance(lsim_bulksms_client: 'LSIMBulkSMSClientClass'):
    assert lsim_bulksms_client.check_balance().body.units == 6
