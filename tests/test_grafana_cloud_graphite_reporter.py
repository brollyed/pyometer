from unittest import TestCase

from pyometer import metric_key
from reporter.grafana_cloud_graphite_reporter import _format_metric_name


class TestGrafanaCloudGraphiteReporter(TestCase):
    def test_format_metric_name(self):
        self.assertEqual("foo", _format_metric_name(metric_key(name=("foo"))))
        self.assertEqual("foo", _format_metric_name(metric_key(name=("foo "))))
        self.assertEqual("foo", _format_metric_name(metric_key(name=("foo."))))
        self.assertEqual("foo-bar", _format_metric_name(metric_key(name=("foo.bar"))))
        self.assertEqual("foo.bar", _format_metric_name(metric_key(name=("foo", "bar"))))
        self.assertEqual("foo.bar.b-a-z", _format_metric_name(metric_key(name=("foo", "bar", " b a   z "))))
        self.assertEqual("foo.ba-r", _format_metric_name(metric_key(name=("foo", "ba'r"))))
        self.assertEqual("fo_o.ba-r", _format_metric_name(metric_key(name=("fo_o", "ba'r"))))
        self.assertEqual("f-o-o.b-a-r", _format_metric_name(metric_key(name=("$%f^o#@ o", "+b()a''r-"))))
        self.assertEqual("foo-bar", _format_metric_name(metric_key(name=("foo - bar"))))
        self.assertEqual("foo-bar", _format_metric_name(metric_key(name=("$  foo -  bar%"))))
