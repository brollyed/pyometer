# pyometer

Python 3 metrics inspired by [Dropwizard Metrics](https://metrics.dropwizard.io/)

## Features

### Metric Keys

Metric keys are used to uniquely identify a single metric. They consist of a `name` (ordered tuple of values)
and `tags` (dictionary of name/value pairs).

```python
from pyometer import metric_key

# Metrics by name
metric_key(name=("project", "metrics"))
# Metrics by tag
metric_key(tags={"env": "production"})
# Metrics by name and tag
metric_key(name=("project", "metrics"), tags={"env": "production"})
```

### MetricRegistry

```python
from pyometer import MetricRegistry, metric_key

registry = MetricRegistry(
    # Metrics created with this registry will be prefixed with this name
    base_key=metric_key(name=("project", "metrics"))
)
```

### ValueGauge

```python
from pyometer import metric_key

# Manually set the value of a gauge with ValueGauge
gauge = registry.value_gauge(key=metric_key(name=("queue_size",)), default=0)
gauge.set_value(100)
```

### CallbackGauge

```python
from pyometer import metric_key


# Automatically pull the value of a gauge with CallbackGauge
def get_queue_size():
    return 4


gauge = registry.callback_gauge(key=metric_key(name=("queue_size",)), callback=get_queue_size)
```

### Timer

```python
from pyometer import metric_key
from pyometer.decorator import timer


@timer(registry=registry, key=metric_key(name=("get_users",)))
def get_users():
    pass  # ... long running task ...
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