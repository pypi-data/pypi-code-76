"""
# Healthchecks (readiness and liveness)
Feature Maturity Status: Alpha
Since this job is CLI, we do not have HTTP healthchecks instead we write files to disk depending on config (i.e. ENV)
See: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/


Example:
```shell
HEALTHCHECK_LIVENESS_FILE=/tmp/liveness
HEALTHCHECK_READINESS_FILE=/tmp/readiness
```

```yaml
livenessProbe:
   initialDelaySeconds: 30
   periodSeconds: 55
   exec:
      command:
      - cat
      - /tmp/liveness
readinessProbe:
   initialDelaySeconds: 30
   periodSeconds: 5
   exec:
      command:
      - cat
      - /tmp/readiness
```
"""
from pathlib import Path

from modular_message_bot.config.config_collection import ConfigCollection


def healthcheck_liveness_file(config: ConfigCollection):
    file = config.get("HEALTHCHECK_LIVENESS_FILE", "")
    if file != "":
        Path(file).touch()


def healthcheck_readiness_file(config: ConfigCollection):
    file = config.get("HEALTHCHECK_READINESS_FILE", "")
    if file != "":
        Path(file).touch()
