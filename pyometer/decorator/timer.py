import asyncio
import functools
import time

from pyometer import MetricRegistry, MetricKey

SUCCESS_METRIC = "success"
FAILURE_METRIC = "failure"


def timer(registry: MetricRegistry,
          key: MetricKey,
          clock=time):
    """
    Function decorator to track the execution time of a function and store the results in a Timer.
    Creates extension metric keys/timers to tracks "success" and "failure" of the function calls.

    :param registry: MetricRegistry for storing results
    :param key: base key of the timer metric
    :param clock: clock to use for gathering time information
    :return:
    """

    def decorator(func):

        def update_result(start_time: float, result: str):
            elapsed_time = clock.time() - start_time
            timer_metric = registry.timer(key.extend_name((result,)))
            timer_metric.update(elapsed_time)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = clock.time()
            try:
                result = func(*args, **kwargs)
                update_result(start_time, SUCCESS_METRIC)
                return result
            except Exception as e:
                update_result(start_time, FAILURE_METRIC)
                raise e

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = clock.time()
            try:
                result = await func(*args, **kwargs)
                update_result(start_time, SUCCESS_METRIC)
                return result
            except Exception as e:
                update_result(start_time, FAILURE_METRIC)
                raise e

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
