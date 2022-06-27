from unittest import TestCase

from pyometer.metric import SupplierGauge, ValueGauge


class TestMetricGauge(TestCase):
    def test_supplier_gauge(self):
        def supplier():
            return 7;

        gauge = SupplierGauge(supplier)

        self.assertEqual(7, gauge.get_value())
        self.assertDictEqual({"value": 7},
                             gauge.metric_values())

    def test_value_gauge(self):
        gauge = ValueGauge(value=13)

        self.assertEqual(13, gauge.get_value())
        self.assertDictEqual({"value": 13},
                             gauge.metric_values())

        gauge.set_value(4)

        self.assertEqual(4, gauge.get_value())
        self.assertDictEqual({"value": 4},
                             gauge.metric_values())
