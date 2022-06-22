from abc import ABC, abstractmethod


class Reporter(ABC):
    @abstractmethod
    def report(self):
        pass

    # TODO add option for starting a periodic reporting thread
    # this frequency will control the 'interval' property of the metric
