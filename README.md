# pyometer

Python 3 metrics inspired by [Dropwizard Metrics](https://metrics.dropwizard.io/)

## Examples

```python
from pyometer import MetricRegistry
from pyometer.metric import ValueGauge, CallbackGauge
from pyometer.reporter import GrafanaCloudGraphiteReporter

# Create a MetricRegistry to track metrics
registry = MetricRegistry(base_name=("foo", "bar"))

# Manually set the value of a gauge with ValueGauge
gauge = registry.add_metric(name=("baz", "queue_size"), metric=ValueGauge())
gauge.set_value(100)


# Automatically pull the value of a gauge with CallbackGauge
def get_queue_size():
    return 4
gauge = registry.add_metric(name=("baz", "queue_size"), metric=CallbackGauge(callback=get_queue_size))


reporter = GrafanaCloudGraphiteReporter

```