from integrify.lsim.client import LSIMClientClass


def test_get_report_get(lsim_client: LSIMClientClass):
    lsim_client.get_report_get(tranid=1)
