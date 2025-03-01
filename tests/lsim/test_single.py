import os
from typing import TYPE_CHECKING

from integrify.lsim.single.schemas.enums import Code
from tests.conftest import live
from tests.lsim.conftest import requires_env

if TYPE_CHECKING:
    from integrify.lsim.single.client import LSIMSingleSMSClientClass


@requires_env()
def test_check_balance(lsim_singlesms_client: 'LSIMSingleSMSClientClass'):
    assert lsim_singlesms_client.check_balance().body.obj == 7


# Report ancaq son 1 həftə üçün keçərlidir. Bir həftə öncədən
# göndərilmiş SMS-lərin statusunu almaq mümkün deyildir
@requires_env('LSIM_TRANS_ID')
@live
def test_get_report_get(lsim_singlesms_client: 'LSIMSingleSMSClientClass'):
    assert (
        lsim_singlesms_client.get_report_get(trans_id=os.getenv('LSIM_TRANS_ID')).body.error_code
        == Code.DELIVERED
    )


@requires_env('LSIM_TRANS_ID')
@live
def test_get_report_post(lsim_singlesms_client: 'LSIMSingleSMSClientClass'):
    assert (
        lsim_singlesms_client.get_report_post(
            trans_id=os.getenv('LSIM_TRANS_ID')
        ).body.delivery_status
        == 'DELIVERED'
    )


# ------------------------------------------------------------------------------------------------ #
# SMS Sending
# ------------------------------------------------------------------------------------------------ #


@requires_env('PHONE_NUMBER_1')
@live
def test_flow_post(lsim_singlesms_client: 'LSIMSingleSMSClientClass'):
    old_balance = lsim_singlesms_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_singlesms_client.send_sms_post(
        msisdn=os.getenv('PHONE_NUMBER_1'),
        text='test',
    ).body.obj

    balance = lsim_singlesms_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_singlesms_client.get_report_post(tranid=tran_id)


@requires_env('PHONE_NUMBER_1')
@live
def test_flow_get(lsim_singlesms_client: 'LSIMSingleSMSClientClass'):
    old_balance = lsim_singlesms_client.check_balance().body.obj

    assert old_balance != -1

    tran_id = lsim_singlesms_client.send_sms_post(
        msisdn=os.getenv('PHONE_NUMBER_1'),
        text='test',
    ).body.obj

    balance = lsim_singlesms_client.check_balance().body.obj

    assert balance + 1 == old_balance

    lsim_singlesms_client.get_report_post(tranid=tran_id)
