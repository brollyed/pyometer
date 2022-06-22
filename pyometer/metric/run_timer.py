from typing import Dict, Any
import time
from pyometer.metric import Metric


class RunTimer(Metric):
    def __init__(self, clock=time):
        self.clock = clock

    def __enter__(self):
        self.start_time = self.clock.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.run_time = self.clock.time() - self.start_time

    def metric_values(self) -> Dict[str, Any]:
        return {"run_time": self.run_time}
