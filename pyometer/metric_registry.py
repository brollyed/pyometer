from typing import List, Callable, Dict

from metric import Counter
from pyometer import MetricKey, metric_key
from pyometer.metric import Metric, ValueGauge, SupplierGauge
from pyometer.metric.timer import Timer
from pyometer.metric_value import MetricValue


class MetricRegistry:
    def __init__(self,
                 base_key: MetricKey = metric_key()):
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

    def value_gauge(self, key: MetricKey, initial_value=None) -> ValueGauge:
        """
        Create or get a ValueGauge.
        :param key:
        :param initial_value:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = ValueGauge(value=initial_value)
        return self._metrics[key]

    def supplier_gauge(self, key: MetricKey, supplier: Callable = None) -> SupplierGauge:
        """
        Create or get a SupplierGauge.
        :param key:
        :param supplier:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = SupplierGauge(supplier=supplier)
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

    def counter(self, key: MetricKey) -> Counter:
        """
        Create or get a Counter.
        :param key:
        :return:
        """
        if key not in self._metrics:
            self._metrics[key] = Counter()
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
                    full_metric_key = temp_metric_key.extend_name(value_name)
                    metric_values.append(MetricValue(key=full_metric_key, value=value))
        return metric_values
