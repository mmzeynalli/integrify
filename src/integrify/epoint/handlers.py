import base64
import json
from decimal import Decimal
from typing import Any, Optional

from integrify.base import APIPayloadHandler, RequestType, ResponseType
from integrify.epoint import env
from integrify.epoint.helper import generate_signature
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)


class BasePayloadHandler(APIPayloadHandler):
    def __init__(self, req_model: type[RequestType], resp_model: type[ResponseType]):
        super().__init__(req_model, resp_model)

    def pre_handle_payload(self, *args, **kwds):
        return {
            'public_key': env.EPOINT_PUBLIC_KEY,
            'language': env.EPOINT_INTERFACE_LANG,
        }

    def post_handle_payload(self, data: dict):
        b64data = base64.b64encode(json.dumps(data).encode()).decode()
        return {
            'data': b64data,
            'signature': generate_signature(b64data),
        }


class PaymentPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, RedirectUrlResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
        **extra: Any,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
        }

        # Optional
        if description:
            data['description'] = description

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            data['error_redirect__url'] = env.EPOINT_FAILED_REDIRECT_URL

        if extra:
            data['other_attr'] = extra

        return data


class GetTransactionStatusPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, TransactionStatusResponseSchema)

    def handle_payload(self, transaction_id: str):
        return {'transaction': transaction_id}


class SaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, RedirectUrlWithCardIdResponseSchema)


class PayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, BaseResponseSchema)

    def handle_payload(self, card_id: str, amount: Decimal, currency: str, order_id: str):
        return {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'card_id': card_id,
        }


class PayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, RedirectUrlWithCardIdResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
        }

        if description:
            data['description'] = description

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            data['error_redirect__url'] = env.EPOINT_FAILED_REDIRECT_URL

        return data


class PayoutPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, BaseResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        description: Optional[str] = None,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'card_id': card_id,
        }

        if description:
            data['description'] = description

        return data


class RefundPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, MinimalResponseSchema)

    def handle_payload(
        self,
        transaction_id: str,
        currency: str,
        amount: Optional[Decimal] = None,
    ):
        data: dict = {'transaction': transaction_id, 'currency': currency}

        if amount:
            data['amount'] = str(amount)  # FIXME

        return data


class SplitPayPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, RedirectUrlResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
        **extra: Any,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'split_user': split_user_id,
            'split_amount': split_amount,
        }

        # Optional
        if description:
            data['description'] = description

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            data['other_attr'] = extra

        return data


class SplitPayWithSavedCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, SplitPayWithSavedCardResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'card_id': card_id,
            'split_user': split_user_id,
            'split_amount': split_amount,
        }

        # Optional
        if description:
            data['description'] = description

        return data


class SplitPayAndSaveCardPayloadHandler(BasePayloadHandler):
    def __init__(self):
        super().__init__(None, RedirectUrlWithCardIdResponseSchema)

    def handle_payload(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ):
        data = {
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'split_user': split_user_id,
            'split_amount': split_amount,
        }

        # Optional
        if description:
            data['description'] = description

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        return data
