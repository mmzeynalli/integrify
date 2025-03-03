import pytest
from httpx import Response


@pytest.fixture(scope='package')
def azericard_transaction_status_response():
    from integrify.azericard.schemas.enums import Action, TrType

    return Response(
        status_code=200,
        json={
            'ACTION': Action.TRANSACTION_SUCCESS,
            'Response code': 'rc',
            'Transaction Status message': 'msg',
            'TERMINAL': '',
            'Card number': '',
            'Transaction amount': 1,
            'Transaction currency': '944',
            'Transaction date': '20250403020100',
            'Transaction state': '',
            'Merchant order id': '',
            'Banks approval code': '',
            'Transaction RRN': '',
            'INT_REF': '',
            'Original transaction TRTYPE': TrType.AUTHORAZATION,
            'Timestamp': '20250403020100',
            'Nonce': '',
            'P_SIGN': '',
        },
    )
