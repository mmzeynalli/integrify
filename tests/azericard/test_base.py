from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING

import pytest
import time_machine
from pydantic_core import ValidationError
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
            m_info={
                'browserScreenHeight': '1080',
                'browserScreenWidth': '1920',
                'browserTZ': '4',
                'mobilePhone': {'cc': '994', 'subscriber': '5555555555'},
            },
        )

        assert (
            req['data']['P_SIGN']
            == '3ab4d6bfc48f888c6f0644f184210c0ae7439ba7cf2fb622a1a09f6003c2713202eefc5ce7101557395d91c3519fa7d90d38c70347311477c033c2af61f60c3f'  # noqa: E501
        )


def test_html_form(azericard_client: 'AzeriCardClientClass'):
    from integrify.azericard.helpers import json_to_html_form

    req = azericard_client.pay(
        amount=1,
        currency='944',
        order='12345678',
        desc='test',
        country='AZ',
    )

    form = json_to_html_form(req)

    assert form.startswith(
        '<form action="https://testmpi.3dsecure.az/cgi-bin/cgi_link" method="POST">'
    )


@pytest.mark.parametrize(
    'amount,exception',
    [(1, does_not_raise()), (2, pytest.raises(ValidationError))],
)
@pytest.mark.key_as_string
def test_signature_verification(amount, exception):
    from integrify.azericard.schemas.callback import TransferCallbackSchema
    from integrify.azericard.schemas.enums import CardStatus

    with exception:
        TransferCallbackSchema.model_validate(
            {
                'OperationID': '1234567890123456',
                'SRN': '1234567890',
                'Amount': amount,
                'Cur': '944',
                'CardStatus': CardStatus.ACTIVE,
                'ReceiverPAN': '0123456789012345',
                'Status': 'pending',
                'Timestamp': '20250403020100',
                'Response Code': '0000',
                'Message': 'Success',
                'Signature': 'c61d54afde515aeba6ae12ab80182324',
            }
        ).model_dump()
