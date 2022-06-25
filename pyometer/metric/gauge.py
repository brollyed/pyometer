from abc import abstractmethod
from typing import Callable, Any, Dict
from pyometer.metric import Metric


class Gauge(Metric):
    @abstractmethod
    def get_value(self):
        pass


class SupplierGauge(Gauge):
    def __init__(self, supplier: Callable):
        self.supplier = supplier

    def get_value(self):
        return self.supplier()

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
