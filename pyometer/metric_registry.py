from typing import List, Tuple, Any, Dict

from pyometer.metric import Metric
from pyometer.metric_value import MetricValue


# TODO tags should be considered as a part of the unique identifier of a metric

class MetricRegistry:
    def __init__(self,
                 base_name: Tuple = None):
        self.base_name = base_name
        self._metrics = {}
        self._tags = {}

    def add_metric(self,
                   name: Tuple,
                   metric: Metric,
                   tags: Dict[str, Any] = None) -> Metric:
        if name in self._metrics:
            raise ValueError(f"Metric already exists for name: {name}")
        self._metrics[name] = metric
        if tags is not None:
            self._tags[name] = tags
        return metric

    def all_metric_values(self) -> List[MetricValue]:
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
