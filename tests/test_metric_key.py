from unittest import TestCase

from pyometer import metric_key


class TestMetricKey(TestCase):
    def test_equal(self):
        # Equal by name
        self.assertEqual(metric_key(name=("foo", "bar")),
                         metric_key(name=("foo", "bar")))
        # Equal by tags
        self.assertEqual(metric_key(tags={"baz": "xyz"}),
                         metric_key(tags={"baz": "xyz"}))
        # Equal by name and tags
        self.assertEqual(metric_key(name=("foo", "bar"), tags={"baz": "xyz"}),
                         metric_key(name=("foo", "bar"), tags={"baz": "xyz"}))

    def test_not_equal(self):
        # Comparing to wrong type
        self.assertNotEqual(metric_key(name=("foo", "bar")),
                            "wrong type")
        # Different names
        self.assertNotEqual(metric_key(name=("foo", "zzz")),
                            metric_key(name=("foo", "bar")))
        # Similar names with different lengths
        self.assertNotEqual(metric_key(name=("foo",)),
                            metric_key(name=("foo", "bar")))
        # Not equal by tags with different names
        self.assertNotEqual(metric_key(tags={"foo": "bar"}),
                            metric_key(tags={"baz": "xyz"}))
        # Not equal by tags with same name but different values
        self.assertNotEqual(metric_key(tags={"baz": "xyz"}),
                            metric_key(tags={"baz": "abc"}))

    def test_hash(self):
        # Hash name
        key = metric_key(name=("foo", "bar"))
        self.assertEqual("abc", {key: "abc"}.get(key))
        # Hash tags
        key = metric_key(tags={"baz": "xyz"})
        self.assertEqual("abc", {key: "abc"}.get(key))
        # Hash name and tags
        key = metric_key(name=("foo", "bar"), tags={"baz": "xyz"})
        self.assertEqual("abc", {key: "abc"}.get(key))

    def test_extend(self):
        # Extend name
        self.assertEqual(metric_key(name=("foo", "bar", "baz")),
                         metric_key(name=("foo", "bar")).extend(metric_key(name="baz")))
        # Extend name
        self.assertEqual(metric_key(name=("foo", "bar", "baz")),
                         metric_key(name=("foo", "bar")).extend_name("baz"))
        # Extend tags
        self.assertEqual(metric_key(tags={"foo": "bar", "baz": "xyz"}),
                         metric_key(tags={"foo": "bar"}).extend(metric_key(tags={"baz": "xyz"})))
        # Extend tags
        self.assertEqual(metric_key(tags={"foo": "bar", "baz": "xyz"}),
                         metric_key(tags={"foo": "bar"}).extend_tags({"baz": "xyz"}))

    def test_bad_types(self):
        self.assertRaises(ValueError, lambda: metric_key(name=5.5))
