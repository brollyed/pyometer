from functools import cache
from typing import Tuple, Any, Dict


class MetricKey:
    def __init__(self,
                 name: Tuple[Any] = (),
                 tags: Dict[str, Any] = {}):
        self.name = name
        self.tags = tags

    @cache
    def __hash__(self):
        hash_tags = self.tags if self.tags is not None else {}
        return hash(self.name,
                    frozenset(hash_tags.items()))

    def __eq__(self, other):
        if not isinstance(other, MetricKey):
            return False
        return self.name == other.name and self.tags == other.tags

    def extend(self, other):
        if not isinstance(other, MetricKey):
            raise ValueError(f"MetricKey.extend expected a MetricKey but got a {type(other)}")
        return MetricKey(name=extend_metric_name(self.name, other.name),
                         tags=extend_metric_tags(self.tags, other.tags))

    def extend_name(self, name: Tuple):
        return self.extend(MetricKey(name=name))

    def extend_tags(self, tags: Dict[str, Any]):
        return self.extend(MetricKey(tags=tags))


def extend_metric_name(base_name: Tuple, other_name: Tuple) -> Tuple:
    return (base_name if base_name is not None else ()) + (other_name if other_name is not None else ())


def extend_metric_tags(base_tags: Dict[str, Any], other_tags: Dict[str, Any]) -> Dict[str, Any]:
    tags = base_tags.copy() if base_tags is not None else {}
    if other_tags is not None:
        tags.update(other_tags)
    return tags


def metric_key(name: Tuple[Any], tags: Dict[str, Any] = None):
    return MetricKey(name=name, tags=tags)
