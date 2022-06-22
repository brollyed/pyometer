from abc import ABC, abstractmethod
from pyometer import MetricRegistry


class Reporter(ABC):

    def __init__(self, registry: MetricRegistry):
        self.registry = registry

    @abstractmethod
    def report(self):
        pass

    # TODO add option for starting a periodic reporting thread
    # this frequency will control the 'interval' property of the metric
