from pyometer import MetricRegistry
from pyometer.reporter import Reporter


class ConsoleReporter(Reporter):
    def __init__(self,
                 registry: MetricRegistry):
        super().__init__(registry)

    def report(self):
        metric_values = self.registry.all_metric_values()
        print("### ConsoleReporter - Metric Values ###")
        for metric_value in metric_values:
            print(f"# name={metric_value.name}; tags={metric_value.tags}; value={metric_value.value}")
