from typing import TYPE_CHECKING

from pytest_mock import MockerFixture

if TYPE_CHECKING:
    from integrify.lsim.client import LSIMClientClass


def test_send_sms_get(lsim_client: 'LSIMClientClass', mocker: MockerFixture):
    lsim_client.send_sms_post(msisdn='994555779018', text='test')


def test_send_sms_post(lsim_client: 'LSIMClientClass', mocker: MockerFixture):
    lsim_client.send_sms_post(msisdn='994555779018', text='test')


def test_check_balance(lsim_client: 'LSIMClientClass'):
    lsim_client.check_balance()


def test_get_report_get(lsim_client: 'LSIMClientClass'):
    lsim_client.get_report_post(tranid=1)


def test_get_report_post(lsim_client: 'LSIMClientClass'):
    lsim_client.get_report_post(tranid=1)
