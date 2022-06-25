from typing import Any

from pyometer import MetricKey


class MetricValue:
    def __init__(self,
                 key: MetricKey,
                 value: Any):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, MetricValue):
            return False
        return self.key == other.key and self.value == other.value

    def __repr__(self):
        return f"MetricValue(key={self.key}, value={self.value})"
