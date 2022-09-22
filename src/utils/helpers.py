import time
import logging 
from functools import wraps

logger = logging.getLogger(__name__)

def exponential_backoff(exc, tries=3, delay=1, backoff=2):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            retry, exp_delay = tries, delay
            while retry > 0:
                try:
                    return f(*args, **kwargs)
                except exc:
                    retry_msg = f'{exc}. Retrying in {exp_delay} seconds... Retries left: {retry}'
                    logger.warning(retry_msg)
                    time.sleep(exp_delay)
                    retry -= 1
                    exp_delay *= backoff
            return f(*args, **kwargs)
        return wrapper
    return decorator