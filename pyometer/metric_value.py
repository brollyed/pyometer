from typing import Any

from pyometer import MetricKey


class MetricValue:
    def __init__(self,
                 key: MetricKey,
                 value: Any):
        self.key = key
        self.value = value
