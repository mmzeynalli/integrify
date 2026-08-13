from datetime import date, datetime
from typing import Annotated, Union

from pydantic import BeforeValidator

IsoDateTime = Annotated[
    Union[str, datetime, None],
    BeforeValidator(lambda v: v.isoformat() if isinstance(v, datetime) else v),
]
"""ISO 8601 date-time format Pydantic field validator."""

IsoDate = Annotated[
    Union[str, datetime, None],
    BeforeValidator(lambda v: v.isoformat() if isinstance(v, date) else v),
]

BoolInt = Annotated[int, BeforeValidator(lambda v: int(bool(v)))]
"""Boolean to integer Pydantic field validator."""
