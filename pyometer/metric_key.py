from typing import Tuple, Any, Dict, Union


class MetricKey:
    def __init__(self,
                 name: Tuple[Any] = (),
                 tags: Dict[str, Any] = {}):
        self.name = name if name is not None else ()
        self.tags = tags if tags is not None else {}

    def __hash__(self):
        return hash((self.name, frozenset(self.tags.items())))

    def __eq__(self, other):
        if not isinstance(other, MetricKey):
            return False
        return self.name == other.name and self.tags == other.tags

    def __str__(self):
        return f"MetricKey(name={self.name}; tags={self.tags})"

    def __repr__(self):
        return self.__str__()

    def extend(self, other):
        if not isinstance(other, MetricKey):
            raise ValueError(f"MetricKey.extend expected a MetricKey but got a {type(other)}")
        return MetricKey(name=_extend_metric_name(self.name, other.name),
                         tags=_extend_metric_tags(self.tags, other.tags))

    def extend_name(self, name: Union[Tuple, str]):
        return self.extend(metric_key(name=name))

    def extend_tags(self, tags: Dict[str, Any]):
        return self.extend(metric_key(tags=tags))


def _extend_metric_name(base_name: Tuple, other_name: Tuple) -> Tuple:
    return (base_name if base_name is not None else ()) + (other_name if other_name is not None else ())


def _extend_metric_tags(base_tags: Dict[str, Any], other_tags: Dict[str, Any]) -> Dict[str, Any]:
    tags = base_tags.copy() if base_tags is not None else {}
    if other_tags is not None:
        tags.update(other_tags)
    return tags


def metric_key(name: Union[Tuple[Any], str] = (),
               tags: Dict[str, Any] = {}) -> MetricKey:
    if isinstance(name, str):
        name = (name,)
    if not isinstance(name, tuple):
        raise ValueError("`name` must be of type `str` or `tuple`")
    if not isinstance(tags, dict):
        raise ValueError("`tags` must be of type `dict`")
    return MetricKey(name=name, tags=tags)
