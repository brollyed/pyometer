from unittest import TestCase

from pyometer import MetricRegistry, metric_key, MetricValue


class TestMetricRegistry(TestCase):
    def test_empty(self):
        registry = MetricRegistry()
        self.assertListEqual([], registry.all_metric_values())

    def test_counter(self):
        registry = MetricRegistry()
        counter = registry.counter(key=metric_key(name="test"))
        counter.increment(100)

        self.assertListEqual([MetricValue(metric_key(("test", "count")), 100)],
                             registry.all_metric_values())

    # TODO value gauge
    # TODO supplier gauge
    # TODO timer