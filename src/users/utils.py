from users import logging
from users import settings

LOGGER = logging.setup_logger(
    'admin',
    level=settings.LOG_LEVEL
)