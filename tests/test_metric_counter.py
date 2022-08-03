from unittest import TestCase

from pyometer.metric import Counter


class TestMetricCounter(TestCase):
    def test_init(self):
        counter = Counter()

        self.assertEqual(0, counter.get_count())
        self.assertDictEqual({"count": 0},
                             counter.metric_values())

    def test_increment(self):
        counter = Counter()
        counter.increment(7)

        self.assertEqual(7, counter.get_count())
        self.assertDictEqual({"count": 7},
                             counter.metric_values())

    def test_decrement(self):
        counter = Counter()
        counter.increment(7)
        counter.decrement(2)

        self.assertEqual(5, counter.get_count())
        self.assertDictEqual({"count": 5},
                             counter.metric_values())

    def test_clear(self):
        counter = Counter()
        counter.increment(7)
        counter.clear()

        self.assertEqual(0, counter.get_count())
        self.assertDictEqual({"count": 0},
                             counter.metric_values())

    def test_set(self):
        counter = Counter()
        counter.set(99)

        self.assertEqual(99, counter.get_count())
        self.assertDictEqual({"count": 99},
                             counter.metric_values())
