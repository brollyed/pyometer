from threading import Lock
from typing import Dict, Any
from pyometer.metric import Metric


class Timer(Metric):
    def __init__(self):
        self.lock = Lock()
        self.total = 0.0
        self.max = None
        self.min = None
        self.count = 0

    def update(self, elapsed_time: float):
        with self.lock:
            self.total += elapsed_time
            if self.min is None or elapsed_time < self.min:
                self.min = elapsed_time
            if self.max is None or elapsed_time > self.max:
                self.max = elapsed_time
            self.count += 1

    def metric_values(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "max": self.max,
            "min": self.min,
            "count": self.count
        }
