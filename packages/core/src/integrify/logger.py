import logging
from collections.abc import Callable
from functools import partial

try:
    import logfire
except ModuleNotFoundError:
    logfire = None


try:
    import loguru
except ModuleNotFoundError:
    loguru = None


LOGGER: Callable = logging.getLogger
LOGURU: Callable = loguru and partial(loguru.logger.bind)
LOGFIRE: Callable = logfire and partial(logfire.with_tags)


LOGGER_FUNCTION = LOGGER
