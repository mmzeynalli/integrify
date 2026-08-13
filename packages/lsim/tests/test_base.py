from datetime import datetime

import time_machine

from integrify.lsim.types import timestamp_to_str


@time_machine.travel('2025-04-03 02:01:00')
def test_timestamp_to_str_with_datetime_now():
    assert timestamp_to_str(datetime.now()) == '2025-04-03 02:01:00'


def test_timestamp_to_str_with_datetime():
    assert timestamp_to_str(datetime(2025, 4, 3, 2, 1, 0)) == '2025-04-03 02:01:00'


def test_timestamp_to_str_with_string():
    assert timestamp_to_str('2025-04-03 02:01:00') == '2025-04-03 02:01:00'
    assert timestamp_to_str('NOW') == 'NOW'


def test_timestamp_to_str_with_invalid_string():
    assert timestamp_to_str('2025-04-03-02:01:00') is None
