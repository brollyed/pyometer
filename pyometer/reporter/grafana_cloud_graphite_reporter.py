import json
import logging
import re
import time
import urllib.parse
import urllib.request
from typing import List, Dict

from pyometer import MetricKey
from pyometer.metric_registry import MetricRegistry
from pyometer.metric_value import MetricValue
from pyometer.reporter import Reporter


class GrafanaCloudGraphiteReporter(Reporter):
    """
    Report metrics to a hosted Grafana Cloud Graphite instance.
    See https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/
    """

    def __init__(self,
                 registry: MetricRegistry,
                 metrics_url: str,
                 instance_id: str,
                 api_key: str,
                 clock=None):
        super().__init__(registry)
        self.metrics_url = metrics_url
        self.instance_id = instance_id
        self.api_key = api_key
        self.clock = clock or time

    def report(self):
        metrics_data = self._collect_metrics()
        if metrics_data:
            request = self._build_request(metrics_data)
            with urllib.request.urlopen(request) as response:
                logging.debug(f"Metrics published to {self.metrics_url}; response code={response.code}; message={response.msg}")

    def _collect_metrics(self) -> List[Dict]:
        timestamp = int(round(self.clock.time()))
        metric_values = self.registry.all_metric_values()
        metric_data = []
        for metric_value in metric_values:
            metric_data.append({
                "name": _format_metric_name(metric_value),
                "interval": 1,  # TODO
                "value": metric_value.value,
                "time": timestamp,
                "tags": self._format_metric_tags(metric_value)
            })

        return json.dumps(metric_data).encode("UTF-8")

    @staticmethod
    def _format_metric_tags(metric_value: MetricValue):
        if metric_value.key.tags is None:
            return None
        metric_tags = []
        for tag_name, tag_value in metric_value.key.tags.items():
            metric_tags.append(f"{tag_name}={tag_value}")
        return metric_tags

    def _build_request(self, metric_data: str):
        return urllib.request.Request(url=self.metrics_url,
                                      headers={
                                          "Authorization": f"Bearer {self.instance_id}:{self.api_key}",
                                          "Content-Type": "application/json"
                                      },
                                      data=metric_data)


def _format_metric_name(metric_key: MetricKey):
    """Sanitize each part of the metric name and separate by periods."""
    return ".".join([_sanitize_metric_name(str(part))
                     for part in metric_key.name])


def _sanitize_metric_name(metric_name: str) -> str:
    # Remove leading and trailing whitespace
    metric_name = metric_name.strip()
    # Remove leading and trailing periods; this is a special character in graphite for separating names
    metric_name = metric_name.strip(".")
    # Replace anything that is not an alphanumeric, underscore with a hyphen
    metric_name = re.sub(r"[^0-9a-zA-Z_]+", "-", metric_name)
    # Remove leading and trailing hyphens
    metric_name = metric_name.strip("-")
    return metric_name
