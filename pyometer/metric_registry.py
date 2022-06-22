from typing import List, Tuple, Any, Dict
from pyometer.metric_value import MetricValue
from pyometer.metric.gauge import Gauge


class MetricRegistry:
    def __init__(self,
                 base_name: Tuple = None):
        self.base_name = base_name
        self._metrics = {}
        self._tags = {}

    def add_gauge(self,
                  name: Tuple,
                  gauge: Gauge,
                  tags: Dict[str, Any] = None) -> Gauge:
        if name in self._metrics:
            raise ValueError(f"Gauge already exists for name: {name}")
        self._metrics[name] = gauge
        if tags is not None:
            self._tags[name] = tags
        return gauge

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
