import logging
from functools import partial
from typing import Callable

try:
    import logfire  # type: ignore[import-not-found]
except ModuleNotFoundError:
    logfire = None  # pylint: disable=invalid-name


try:
    import loguru  # type: ignore[import-not-found]
except ModuleNotFoundError:
    loguru = None  # pylint: disable=invalid-name


LOGGER: Callable = logging.getLogger
LOGURU: Callable = loguru and partial(loguru.logger.bind)
LOGFIRE: Callable = logfire and partial(logfire.with_tags)


LOGGER_FUNCTION = LOGGER
