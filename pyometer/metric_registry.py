from typing import List, Callable, Dict

from pyometer import MetricKey
from pyometer.metric import Metric, ValueGauge, CallbackGauge
from pyometer.metric.timer import Timer
from pyometer.metric_value import MetricValue


class MetricRegistry:
    def __init__(self,
                 base_key: MetricKey):
        self._base_key = base_key
        self._metrics: Dict[MetricKey, Metric] = {}

    def register(self, key: MetricKey, metric: Metric) -> Metric:
        """
        Register a new metric with the registry.
        :param key:
        :param metric:
        :return:
        """
        if key in self._metrics:
            raise ValueError(f"Metric already exists for key: {key}")
        self._metrics[key] = metric
        return metric

    def value_gauge(self, key: MetricKey, default=None) -> ValueGauge:
        """
        Create or get a ValueGauge.
        :param key:
        :param default:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = ValueGauge(value=default)
        return self._metrics[key]

    def callback_gauge(self, key: MetricKey, callback: Callable = None) -> CallbackGauge:
        """
        Create or get a CallbackGauge.
        :param key:
        :param callback:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = CallbackGauge(callback=callback)
        return self._metrics[key]

    def timer(self, key: MetricKey) -> Timer:
        """
        Create or get a Timer.
        :param key:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = Timer()
        return self._metrics[key]

    def all_metric_values(self) -> List[MetricValue]:
        """
        Get a snapshot of all registered metric values.
        :return:
        """
        metric_values = []
        for metric_key in self._metrics.keys():
            metric = self._metrics[metric_key]
            temp_metric_key = self._base_key.extend(metric_key)
            for value_name, value in metric.metric_values().items():
                if value is not None:
                    full_metric_key = temp_metric_key.extend_name((value_name,))
                    metric_values.append(MetricValue(key=full_metric_key, value=value))
        return metric_values
