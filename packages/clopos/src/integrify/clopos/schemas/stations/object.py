from integrify.clopos.schemas.common.object import Timestamp
from integrify.utils import UnsetOrNoneField


class Station(Timestamp):
    id: int
    """Unique identifier"""

    name: str
    """Name of the station"""

    status: int
    """1 = active, 0 = inactive"""

    type: UnsetOrNoneField[int]
    """Type of the station"""

    printable: UnsetOrNoneField[int]
    """Whether the station is printable or not"""

    can_print: UnsetOrNoneField[bool]
    """Can be redirected to a printer"""

    reminder_enabled: UnsetOrNoneField[bool]
    """Is reminder notification on?"""

    meta: UnsetOrNoneField[dict]
    """Additional settings and visibility info"""

    description: UnsetOrNoneField[str]
    """Optional description"""
