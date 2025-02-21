import os
from typing import TYPE_CHECKING

from integrify.lsim.schemas.enums import Code
from tests.conftest import live
from tests.lsim.conftest import requires_env

if TYPE_CHECKING:
    from integrify.lsim.client import LSIMClientClass


@requires_env()
def test_check_balance(lsim_client: 'LSIMClientClass'):
    assert lsim_client.check_balance().body.obj == 2


@requires_env('LSIM_TRANS_ID')
def test_get_report_get(lsim_client: 'LSIMClientClass'):
    assert (
        lsim_client.get_report_get(trans_id=os.getenv('LSIM_TRANS_ID')).body.error_code
        == Code.DELIVERED
    )


@requires_env('LSIM_TRANS_ID')
def test_get_report_post(lsim_client: 'LSIMClientClass'):
    assert (
        lsim_client.get_report_post(trans_id=os.getenv('LSIM_TRANS_ID')).body.delivery_status
        == 'DELIVERED'
    )


@requires_env()
@live
def test_flow_post(lsim_client: 'LSIMClientClass'):
    old_balance = lsim_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_client.send_sms_post(msisdn='994555779018', text='test').body.obj

    balance = lsim_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_client.get_report_post(tranid=tran_id)


@requires_env()
@live
def test_flow_get(lsim_client: 'LSIMClientClass'):
    old_balance = lsim_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_client.send_sms_post(msisdn='994555779018', text='test').body.obj

    balance = lsim_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_client.get_report_post(tranid=tran_id)
