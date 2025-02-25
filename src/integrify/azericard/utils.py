from datetime import datetime
from typing import Annotated, Union

from pydantic import BeforeValidator, Field


def timestamp_to_str(timestamp: Union[datetime, str]) -> str:
    """Serialize etdikdə timestamp-i AzeriCard formatına salan funksiya"""

    if isinstance(timestamp, datetime):
        return timestamp.strftime('%Y%m%d%H%M%S')

    return timestamp


def str_to_timestamp(timestamp: Union[datetime, str]) -> datetime:
    """Deserialize etdikdə timestamp-i datetime obyektine salan funksiya"""

    if isinstance(timestamp, datetime):
        return timestamp

    return datetime.strptime(timestamp, '%Y%m%d%H%M%S')


TimeStampOut = Annotated[
    str,
    Field(default_factory=datetime.now, validate_default=True),
    BeforeValidator(timestamp_to_str),
    'AzeriCard-a göndəriləcək timestamp (YYMMDDhhmmss formatına salınır)',
]


TimeStampIn = Annotated[
    datetime,
    BeforeValidator(str_to_timestamp),
    'AzeriCard-dan gələn, python datetime-a konvert olunan timestamp',
]
