from unittest import TestCase

from metric.timer import Timer


class TestMetricTimer(TestCase):
    def test_init(self):
        timer = Timer()

        self.assertDictEqual({
            "count": 0,
            "max": None,
            "min": None,
            "total": 0
        }, timer.metric_values())

    def test_update(self):
        timer = Timer()
        timer.update(3.14159)

        self.assertDictEqual({
            "count": 1,
            "max": 3.14159,
            "min": 3.14159,
            "total": 3.14159
        }, timer.metric_values())

    def test_many_updates(self):
        timer = Timer()
        timer.update(3.1)
        timer.update(4.7)
        timer.update(2.9)

        metric_values = timer.metric_values()
        self.assertEqual(3, metric_values["count"])
        self.assertEqual(4.7, metric_values["max"])
        self.assertEqual(2.9, metric_values["min"])
        self.assertAlmostEqual(10.7, metric_values["total"])
