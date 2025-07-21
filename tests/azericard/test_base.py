from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING

import pytest
import time_machine
from pydantic_core import ValidationError
from pytest_mock import MockerFixture

from tests.azericard.conftest import requires_env

if TYPE_CHECKING:
    from integrify.azericard.client import AzeriCardClientClass


@requires_env()
@time_machine.travel('2025-04-03 02:01:00')
def test_psign_generation(azericard_client: 'AzeriCardClientClass', mocker: MockerFixture):
    from integrify.azericard.schemas.enums import AuthorizationType

    with mocker.patch('random.getrandbits', return_value=0xFFEEDDCCBBAA99887766554433221100):
        req = azericard_client.authorization(
            1,  # amount
            'AZN',  # currency
            '12345678',  # order
            trtype=AuthorizationType.DIRECT,
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
            == '715716a0d73cac9f69878baee497497c6b24a61c59c7cd66e1c99a13e2fb9cd18dd71fc77e4ba54d152de15055c4c63814d358cbdd12f990a540d5e36bfd8fa607d519c7856536c82393ff2e50375e3bc88263277096c38944a9682e706c931d735febee882ed9bb7698a3a1961c06a4fb2d4e1a35d3e94ecf2352002ac1dcc33c26d9821e96c266f23e952400e7dd358d3c5fddb68c698ceb459666d1b81ade0a78bb59f5b56efdf8e8cea8ff82d88b6e42e55d569c89b608937a10c2848a73293340edc1abd94205471367f4e632e4f32e03d1cc90f9b4d9ae33313f4692975eabf6d24042314d492da54261360ae1940c31e5a6d2fcd701fb85a985f41d31'  # noqa: E501
        )


@requires_env()
def test_html_form(azericard_client: 'AzeriCardClientClass'):
    from integrify.azericard.helpers import json_to_html_form
    from integrify.azericard.schemas.enums import AuthorizationType

    req = azericard_client.authorization(
        amount=1,
        currency='AZN',
        order='12345678',
        desc='test',
        country='AZ',
        trtype=AuthorizationType.DIRECT,
    )

    form = json_to_html_form(req)

    assert form.startswith(
        '<form name="azericard_form" action="https://testmpi.3dsecure.az/cgi-bin/cgi_link" method="POST">'  # noqa: E501
    )


@pytest.mark.parametrize(
    'amount,exception',
    [(1, does_not_raise()), (2, pytest.raises(ValidationError))],
)
def test_signature_verification(amount, exception):
    from integrify.azericard.schemas.callback import TransferCallbackSchema
    from integrify.azericard.schemas.enums import CardStatus

    with exception:
        TransferCallbackSchema.model_validate(
            {
                'OperationID': '1234567890123456',
                'SRN': '1234567890',
                'Amount': amount,
                'Cur': 'AZN',
                'CardStatus': CardStatus.ACTIVE,
                'ReceiverPAN': '0123456789012345',
                'Status': 'pending',
                'Timestamp': '20250403020100',
                'Response Code': '0000',
                'Message': 'Success',
                'Signature': 'bf46acdb8fe9ecc6ba784a3427de88d1',
            }
        ).model_dump()
