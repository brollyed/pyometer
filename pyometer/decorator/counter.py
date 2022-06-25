import asyncio
import functools

from pyometer import MetricRegistry, MetricKey

SUCCESS_METRIC = "success"
FAILURE_METRIC = "failure"


def counter(registry: MetricRegistry, key: MetricKey):
    """
    Function decorator to track the count function executions and store the results in a Counter metric.
    Creates extension metric keys/counters to track "success" and "failure" of the function calls.

    :param registry: MetricRegistry for storing results
    :param key: base key of the counter metric
    :return:
    """

    def decorator(func):

        def update_result(result: str):
            counter_metric = registry.counter(key.extend_name((result,)))
            counter_metric.increment()

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                update_result(SUCCESS_METRIC)
                return result
            except Exception as e:
                update_result(FAILURE_METRIC)
                raise e

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                update_result(SUCCESS_METRIC)
                return result
            except Exception as e:
                update_result(FAILURE_METRIC)
                raise e

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
