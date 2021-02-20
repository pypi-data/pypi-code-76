"""
# Datetime Input Module
This is a wrapper for Python Date. Format options come from Python date function

Example Simple Input:
```yaml
- code: datetime
  parameters:
    var: date
    format: '%c'
```

Example Advanced Input:
```yaml
- code: datetime
  parameters:
    var: date
    format: '%c'
    # Add some time (see timedelta in https://docs.python.org/3/library/datetime.html)
    add:
       hours: 1
       minutes: 10
    # Subtract some time (see timedelta in https://docs.python.org/3/library/datetime.html)
    sub:
       days: 2
       seconds: 50
```
"""
from datetime import datetime, timedelta

import pytz

from modular_message_bot.config.constants import SCHEDULER_TIMEZONE_CFG_KEY
from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection


class DateTimeInput(AbstractSimpleInputHandler):
    @classmethod
    def get_code(cls) -> str:
        return "datetime"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        # Settings
        var = str(parameters.get("var"))
        timezone = str(parameters.get("timezone", self.config.get(SCHEDULER_TIMEZONE_CFG_KEY)))
        date_format = str(parameters.get("format", "%c"))
        add = parameters.get("add", {})
        sub = parameters.get("sub", {})

        tz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        dt = tz.localize(dt)
        dt = dt + timedelta(**add)
        dt = dt - timedelta(**sub)
        dt.astimezone(tz).strftime(date_format)

        value = dt.strftime(date_format)
        job_run_vars_collection.interpolate(var, value, self.get_code())
