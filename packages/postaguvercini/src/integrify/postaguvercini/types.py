from datetime import datetime
from typing import Annotated

from pydantic import BeforeValidator, Field

FORMAT = '%Y%m%d %H:%M'


def timestamp_to_str(value: str | datetime) -> str | None:
    """Verilmiş datetime-i uyğun string formata salır.
    Əgər string şəklində verilibsə, format uyğunluğu yoxlanılır."""

    if isinstance(value, str):
        try:
            datetime.strptime(value, FORMAT)
        except ValueError:
            return None

        return value

    return value.strftime(FORMAT)


DateTime = Annotated[
    str | datetime,
    Field(default=None),
    BeforeValidator(timestamp_to_str),
    'PostaGuvercin-ə göndəriləcək timestamp (YYYY-mm-DD HH:MM:SS formatına salınır)',
]
