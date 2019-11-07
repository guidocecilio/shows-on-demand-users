import logging
import os
import sys


LOG_FORMAT = "%(asctime)-15s [%(process)s] %(levelname)-5s <%(name)s> %(filename)s:%(lineno)-4d Corr_Id: %(correlation_id)s %(message)s"


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.correlation_id = ''
        return True

# pylint: disable=too-many-arguments
def setup_logger(
        logger_name,
        level='INFO',
        stream=sys.stderr,
        log_format=None,
        extra_handlers=()
):
    """ Sets up given logger with a StreamHandler (default is stderr) """
    if isinstance(logger_name, str):
        logger = logging.getLogger(logger_name)

    if isinstance(level, str):
        level = logging.getLevelName(level)

    logger.handlers = []  # make sure there are no old handlers
    logger.setLevel(level)

    formatter = logging.Formatter(log_format or LOG_FORMAT)

    extra_handlers = [logging.StreamHandler(stream), ] + list(extra_handlers)

    for handler in extra_handlers:
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    cfilter = ContextFilter()
    logger.addFilter(cfilter)
    return logger


LOGGER = setup_logger(
    'users',
    level=os.environ.get('LOG_LEVEL', 'INFO')
)