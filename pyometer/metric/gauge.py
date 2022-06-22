from abc import abstractmethod
from typing import Callable, Any, Dict
from pyometer.metric import Metric


class Gauge(Metric):
    @abstractmethod
    def get_value(self):
        pass


class CallbackGauge(Gauge):
    def __init__(self, callback: Callable):
        self.callback = callback

    def get_value(self):
        return self.callback()

    def metric_values(self) -> Dict[str, Any]:
        return {"value": self.get_value()}


class ValueGauge(Gauge):
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def metric_values(self) -> Dict[str, Any]:
        return {"value": self.get_value()}
