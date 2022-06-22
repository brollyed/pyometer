from typing import Any, Dict, Tuple


class MetricValue:
    def __init__(self,
                 name: Tuple,
                 tags: Dict[str, Any],
                 value: Any):
        self.name = name
        self.tags = tags
        self.value = value
