from typing import List, Tuple, Any, Dict, Callable

from pyometer.metric import Metric, ValueGauge, CallbackGauge
from pyometer.metric.timer import Timer
from pyometer.metric_value import MetricValue


# TODO tags should be considered as a part of the unique identifier of a metric

class MetricRegistry:
    def __init__(self,
                 base_name: Tuple = None):
        self.base_name = base_name
        self._metrics = {}
        self._tags = {}

    def register(self,
                 name: Tuple,
                 metric: Metric,
                 tags: Dict[str, Any] = None) -> Metric:
        """
        Register a new metric with the registry.
        :param name:
        :param metric:
        :param tags:
        :return:
        """
        if name in self._metrics:
            raise ValueError(f"Metric already exists for name: {name}")
        self._metrics[name] = metric
        if tags is not None:
            self._tags[name] = tags
        return metric

    def value_gauge(self, name: Tuple, tags: Dict[str, Any] = None, default=None) -> ValueGauge:
        """
        Create or get a ValueGauge.
        :param name:
        :param tags:
        :param default:
        :return:
        """
        if name not in self._metrics:
            self._metrics[name] = ValueGauge(value=default)
            if tags is not None:
                self._tags[name] = tags
        return self._metrics[name]

    def callback_gauge(self, name: Tuple, tags: Dict[str, Any] = None, callback: Callable = None) -> CallbackGauge:
        """
        Create or get a CallbackGauge.
        :param name:
        :param tags:
        :param callback:
        :return:
        """
        if name not in self._metrics:
            self._metrics[name] = CallbackGauge(callback=callback)
            if tags is not None:
                self._tags[name] = tags
        return self._metrics[name]

    def timer(self, name: Tuple, tags: Dict[str, Any] = None) -> Timer:
        """
        Create or get a Timer.
        :param name:
        :param tags:
        :return:
        """
        if name not in self._metrics:
            self._metrics[name] = Timer()
            if tags is not None:
                self._tags[name] = tags
        return self._metrics[name]

    def all_metric_values(self) -> List[MetricValue]:
        """
        Get a snapshot of all registered metric values.
        :return:
        """
        metric_values = []
        for name in self._metrics.keys():
            tags = self._tags[name] if name in self._tags else None
            metric = self._metrics[name]
            for value_name, value in metric.metric_values().items():
                full_name = (self.base_name if self.base_name is not None else ()) + name + (value_name,)
                if value is not None:
                    metric_values.append(
                        MetricValue(name=full_name,
                                    tags=tags,
                                    value=value))
        return metric_values
