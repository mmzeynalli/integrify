from typing import TYPE_CHECKING

from integrify.lsim.schemas.enums import Code
from tests.conftest import github

if TYPE_CHECKING:
    from integrify.lsim.client import LSIMClientClass


@github
def test_check_balance(lsim_client: 'LSIMClientClass'):
    assert lsim_client.check_balance().body.obj == 2


@github
def test_get_report_get(lsim_client: 'LSIMClientClass'):
    assert lsim_client.get_report_get(trans_id=2275731548).body.error_code == Code.DELIVERED


@github
def test_get_report_post(lsim_client: 'LSIMClientClass'):
    assert lsim_client.get_report_post(trans_id=2275813585).body.delivery_status == 'DELIVERED'
