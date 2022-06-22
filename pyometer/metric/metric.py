from abc import ABC, abstractmethod
from typing import Any, Dict


class Metric(ABC):
    @abstractmethod
    def metric_values(self) -> Dict[str, Any]:
        pass
