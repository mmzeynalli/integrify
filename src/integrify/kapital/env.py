import os
from enum import Enum
from typing import Literal, Optional
from warnings import warn


KAPITAL_BASE_URL: str = os.getenv("KAPITAL_BASE_URL")
KAPITAL_USERNAME: str = os.getenv("KAPITAL_USERNAME")
KAPITAL_PASSWORD: str = os.getenv("KAPITAL_PASSWORD")

KAPITAL_INTERFACE_LANG: str = os.getenv("KAPITAL_INTERFACE_LANG", "az")
KAPITAL_REDIRECT_URL: Optional[str] = os.getenv("KAPITAL_REDIRECT_URL")


if not KAPITAL_BASE_URL or not KAPITAL_USERNAME or not KAPITAL_PASSWORD:
    warn(
        "KAPITAL_BASE_URL/KAPITAL_USERNAME/KAPITAL_PASSWORD mühit dəyişənlərinə dəyər verməsəniz "
        "sorğular çalışmayacaq!"
    )


class API(str, Enum):
    CREATE_ORDER: Literal["/api/order"] = "/api/order"
    SAVE_CARD: Literal["/api/order"] = "/api/order"
    PAY_WITH_SAVED_CARD: Literal["/api/order/{order_id}/exec-tran"] = (
        "/api/order/{order_id}/exec-tran"
    )
    REVERSE: Literal["/api/order/{order_id}/exec-tran"] = (
        "/api/order/{order_id}/exec-tran"
    )
    REFUND: Literal["/api/order/{order_id}/exec-tran"] = (
        "/api/order/{order_id}/exec-tran"
    )
    GET_ORDER_DETAILS: Literal["/api/order/{order_id}"] = "/api/order/{order_id}"


__all__ = [
    "KAPITAL_BASE_URL",
    "KAPITAL_USERNAME",
    "KAPITAL_PASSWORD",
    "KAPITAL_INTERFACE_LANG",
    "KAPITAL_REDIRECT_URL",
    "API",
]
