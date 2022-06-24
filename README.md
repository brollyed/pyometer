# pyometer

Python 3 metrics inspired by [Dropwizard Metrics](https://metrics.dropwizard.io/)

## Examples

### MetricRegistry
### TODO update all with key stuff
```python
from pyometer import MetricRegistry

registry = MetricRegistry(
    base_name=("foo", "bar")  # Metrics created with this registry will be prefixed with this name
)
```

### ValueGauge

```python
# Manually set the value of a gauge with ValueGauge
gauge = registry.value_gauge(name=("baz", "queue_size"), default=0)
gauge.set_value(100)
```

### CallbackGauge

```python
# Automatically pull the value of a gauge with CallbackGauge
def get_queue_size():
    return 4


gauge = registry.callback_gauge(name=("baz", "queue_size"), callback=get_queue_size)
```

### Timer

```python
from pyometer.decorator import timer
import time
import random

@timer(registry=registry, name=("baz"))
def do_hard_work():
    time.sleep(random.randint(5, 10))
```

### Reporters

#### GrafanaCloudGraphiteReporter

```python
from pyometer.reporter import GrafanaCloudGraphiteReporter

# Create a reporter for a Grafana-hosted Graphite instance
reporter = GrafanaCloudGraphiteReporter(registry=registry,
                                        metrics_url="<metrics url>",
                                        instance_id="<instance id>",
                                        api_key="<api key>")

# Manually push metrics
reporter.report()
```