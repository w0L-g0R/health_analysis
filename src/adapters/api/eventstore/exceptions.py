import functools
import logging

from src.config.config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except KeyboardInterrupt as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise e

    return wrapper
