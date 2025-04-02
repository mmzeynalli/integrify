from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockerFixture

if TYPE_CHECKING:
    from integrify.azericard.client import AzeriCardClientClass


def test_pay_and_save_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.pay_and_save_card(amount=1, currency='AZN', order='12345678', desc='desc')


def test_pay_with_saved_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.pay_with_saved_card(
        amount=1,
        currency='AZN',
        order='12345678',
        desc='desc',
        token='*' * 28,
    )


def test_block(azericard_client: 'AzeriCardClientClass'):
    azericard_client.block(amount=1, currency='AZN', order='12345678', desc='desc')


def test_block_and_save_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.block_and_save_card(amount=1, currency='AZN', order='12345678', desc='desc')


def test_block_with_saved_card(azericard_client: 'AzeriCardClientClass'):
    azericard_client.block_with_saved_card(
        amount=1,
        currency='AZN',
        order='12345678',
        desc='desc',
        token='*' * 28,
    )


def test_accept_blocked_payment(azericard_client: 'AzeriCardClientClass'):
    azericard_client.accept_blocked_payment(
        amount=1,
        currency='AZN',
        order='12345678',
        rrn='rrnrrnrrnrrn',
        int_ref='int_ref',
    )


def test_reverse_blocked_payment(azericard_client: 'AzeriCardClientClass'):
    azericard_client.reverse_blocked_payment(
        amount=1,
        currency='AZN',
        order='12345678',
        rrn='rrnrrnrrnrrn',
        int_ref='int_ref',
    )


def test_cancel_blocked_payment(azericard_client: 'AzeriCardClientClass'):
    azericard_client.cancel_blocked_payment(
        amount=1,
        currency='AZN',
        order='12345678',
        rrn='rrnrrnrrnrrn',
        int_ref='int_ref',
    )


def test_get_transaction_status(
    azericard_client: 'AzeriCardClientClass',
    mocker: MockerFixture,
    azericard_transaction_status_response,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=azericard_transaction_status_response,
    ):
        azericard_client.get_transaction_status(tran_trtype='1', order='12345678')


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
