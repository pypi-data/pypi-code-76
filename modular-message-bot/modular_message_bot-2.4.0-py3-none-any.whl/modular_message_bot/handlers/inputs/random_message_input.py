"""
# Random Message Input Module
This takes random vars and adds them to another var
i.e. Take all job vars with a code prefix of "x" and add a random one to var "y"

```yaml
- code: random_message
  parameters:
     match:
        x: "^y"
```
"""
import logging
import re
from random import choice as random_choice

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection

logger = logging.getLogger(__name__)


class RandomMessageInput(AbstractSimpleInputHandler):
    @classmethod
    def get_code(cls) -> str:
        return "random_message"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        # Find all the matching job strings
        for var, code_regex in parameters.get("match", {}).items():
            matching_job_vars = []
            job_run_var: JobRunVar
            for job_run_var in job_run_vars_collection.get_all():
                matches = re.search(code_regex, job_run_var.code)
                if matches is not None and isinstance(job_run_var.value, str):
                    matching_job_vars.append(job_run_var.value)

            if len(matching_job_vars) <= 0:
                logger.warning(f"{self.get_code()}: No matching job strings")
                return

            # Pick a random string
            matching_job_var: str = random_choice(matching_job_vars)

            # Put the random message into the message holder
            job_run_vars_collection.interpolate(var, matching_job_var, self.get_code())
