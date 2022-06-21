from abc import ABC, abstractmethod


class Reporter(ABC):
    @abstractmethod
    def report(self):
        pass
