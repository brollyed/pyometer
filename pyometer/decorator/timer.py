import asyncio
import functools
from typing import Dict, Tuple
import time
from pyometer import MetricRegistry

SUCCESS_METRIC = "success"
FAILURE_METRIC = "failure"


def timer(registry: MetricRegistry,
          name: Tuple,
          tags: Dict[str, str] = None,
          clock=time):
    """
    Function decorator to track the execution time of a function and store the results in a Timer.
    :param registry: MetricRegistry for storing results
    :param name: base name of the timer metric
    :param tags: tags of the timer metric
    :param clock: clock to use for gathering time information
    :return:
    """

    def decorator(func):

        def update_result(start_time: float, result: str):
            elapsed_time = clock.time() - start_time
            timer_metric = registry.timer(name=name + (result,), tags=tags)
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
