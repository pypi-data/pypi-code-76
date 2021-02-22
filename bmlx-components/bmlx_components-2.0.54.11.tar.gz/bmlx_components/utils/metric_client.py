import requests
import json

PROMETHEUS_URL = "http://alert-store.bigo.sg:8881/insert/42/prometheus"


def report_metric_to_prometheus(name, value, ts, labels, url=PROMETHEUS_URL):
    data = {"n": name, "ls": labels, "ts": int(ts), "v": float(value)}
    headers = {"content-type": "application/json"}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    resp.raise_for_status()
