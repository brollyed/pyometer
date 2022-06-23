from typing import Tuple, Any, Dict


class MetricKey:
    def __init__(self,
                 name: Tuple[Any],
                 tags: Dict[str, Any] = None):
        self.name = name
        self.tags = tags


def metric_key(name: Tuple[Any], tags: Dict[str, Any] = None):
    pass  # TODO
