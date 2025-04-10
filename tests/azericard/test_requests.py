from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockerFixture

from integrify.azericard.schemas.enums import AuthorizationResponseType, AuthorizationType
from tests.azericard.conftest import requires_env

if TYPE_CHECKING:
    from integrify.azericard.client import AzeriCardClientClass


@requires_env()
def test_pay_and_save_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.auth_and_save_card(
        amount=1,
        currency='AZN',
        order='12345678',
        desc='desc',
        trtype=AuthorizationType.DIRECT,
    )


@requires_env()
def test_pay_with_saved_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.auth_with_saved_card(
        amount=1,
        currency='AZN',
        order='12345678',
        desc='desc',
        token='*' * 28,
        trtype=AuthorizationType.DIRECT,
    )


@requires_env()
def test_accept_blocked_payment(azericard_client: 'AzeriCardClientClass'):
    azericard_client.finalize(
        amount=1,
        currency='AZN',
        order='12345678',
        rrn='rrnrrnrrnrrn',
        int_ref='int_ref',
        trtype=AuthorizationResponseType.ACCEPT_PAYMENT,
    )


@requires_env()
def test_get_transaction_status(
    azericard_client: 'AzeriCardClientClass',
    mocker: MockerFixture,
    azericard_transaction_status_response,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=azericard_transaction_status_response,
    ):
        azericard_client.get_transaction_status(
            tran_trtype=AuthorizationType.DIRECT,
            order='12345678',
        )


@requires_env()
@pytest.mark.key_as_string
def test_start_transfer(azericard_client: 'AzeriCardClientClass'):
    azericard_client.transfer_start(
        merchant='merchant',
        srn='srn',
        amount=1,
        cur='AZN',
        receiver_credentials='creds',
        redirect_link='link',
    )


# def test_confirm_transfer(azericard_client: 'AzeriCardClientClass'):
#     azericard_client.transfer_confirm(
#         merchant='merchant',
#         srn='srn',
#         amount=1,
#         cur='AZN',
#         receiver_credentials='creds',
#         redirect_link='link',
#     )
