import logging
from typing import List, Dict
import time
import urllib.request
import urllib.parse
import json
from pyometer.metric_registry import MetricRegistry
from pyometer.reporter import Reporter


class GrafanaCloudGraphiteReporter(Reporter):
    """
    Report metrics to a hosted Grafana Cloud Graphite instance.
    """

    def __init__(self,
                 registry: MetricRegistry,
                 metrics_url: str,
                 instance_id: str,
                 api_key: str,
                 clock=None):
        self.registry = registry
        self.metrics_url = metrics_url
        self.instance_id = instance_id
        self.api_key = api_key
        self.clock = clock or time

    def report(self):
        metrics_data = self._collect_metrics()
        if metrics_data:
            request = self._build_request()
            with urllib.request.urlopen(request) as response:
                logging.debug(f"Metrics published to {self.metrics_url}; response code={response.code}; message={response.msg}")

    def _collect_metrics(self) -> List[Dict]:
        timestamp = int(round(self.clock.time()))
        metrics = self.registry.dump_metrics()
        metrics_values = []
        for key in metrics.keys():
            for value_key in metrics[key].keys():
                metrics_values.append({
                    "name": f"{key}.{value_key}",
                    "interval": 1,  # TODO
                    "value": metrics[key][value_key],
                    "time": timestamp,
                    "tags": None
                })

        return metrics_values

    def _build_request(self, metrics_data: List[Dict]):
        return urllib.request.Request(url=self.metrics_url,
                                      headers={
                                          "Authorization": f"Bearer {self.instance_id}:{self.api_key}",
                                          "Content-Type": "application/json"
                                      },
                                      data=json.dumps(metrics_data).encode("UTF-8"))
