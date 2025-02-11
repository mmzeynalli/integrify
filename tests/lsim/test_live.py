from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from integrify.lsim.client import LSIMClientClass


@pytest.mark.live
def test_flow_post(lsim_client: 'LSIMClientClass'):
    old_balance = lsim_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_client.send_sms_post(msisdn='994555779018', text='test').body.obj

    balance = lsim_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_client.get_report_post(tranid=tran_id)


@pytest.mark.live
def test_flow_get(lsim_client: 'LSIMClientClass'):
    old_balance = lsim_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_client.send_sms_post(msisdn='994555779018', text='test').body.obj

    balance = lsim_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_client.get_report_post(tranid=tran_id)
