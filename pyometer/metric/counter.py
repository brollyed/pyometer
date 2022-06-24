from threading import Lock
from typing import Any, Dict

from metric import Metric


class Counter(Metric):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def _change_by(self, value: int):
        with self.lock:
            self.count += value

    def increment(self, value: int = 1):
        self._change_by(value)

    def decrement(self, value: int = 1):
        self._change_by(-value)

    def clear(self):
        with self.lock:
            self.count = 0

    def get_count(self):
        return self.count

    def metric_values(self) -> Dict[str, Any]:
        return {"count": self.count}
