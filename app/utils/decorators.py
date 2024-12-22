import time
from functools import wraps

from app.utils.logger import configure_logger

log = configure_logger()


def record_execution_time():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start_time = time.perf_counter()
            ret = func(*args, **kwargs)
            duration = (time.perf_counter() - start_time) * 1000
            log.info(
                f"Function: {func.__module__}:{func.__name__} \
                    Execution Time: {duration} ms \
                        args: {args} kwargs: {kwargs}"
            )
            return ret

        return inner

    return wrapper
