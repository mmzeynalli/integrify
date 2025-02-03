from typing import TYPE_CHECKING

import time_machine
from pytest_mock import MockerFixture

if TYPE_CHECKING:
    from integrify.azericard.client import AzeriCardClientClass


@time_machine.travel('2025-04-03 02:01:00')
def test_psign_generation(azericard_client: 'AzeriCardClientClass', mocker: MockerFixture):
    with mocker.patch('random.getrandbits', return_value=0xFFEEDDCCBBAA99887766554433221100):
        req = azericard_client.pay(
            1,  # amount
            '944',  # currency
            '12345678',  # order
            desc='test',
            country='AZ',
        )

        assert (
            req.body['data']['P_SIGN']
            == 'a6870b8b80540304b3100997db51ec8add1727ed9feff9ea79f06d99399dedb4'
        )


def test_html_form(azericard_client: 'AzeriCardClientClass'):
    from integrify.azericard.utils import json_to_html_form

    req = azericard_client.pay(
        amount=1,
        currency='944',
        order='12345678',
        desc='test',
        country='AZ',
    )

    form = json_to_html_form(req.body)

    assert form.startswith(
        '<form action="https://testmpi.3dsecure.az/cgi-bin/cgi_link" method="POST">'
    )
