"""
# Chance
Random chance of running a job

Example Pre:
```yaml
- code: chance
  params:
     percentage: 50
```
"""
import logging
from random import randint

from modular_message_bot.handlers.pres.abstract_pre_handler import AbstractPreHandler
from modular_message_bot.models.job_run import JobRunVarCollection

logger = logging.getLogger(__name__)


class ChancePre(AbstractPreHandler):
    @classmethod
    def get_code(cls) -> str:
        return "chance"

    def run(self, parameters: dict, job_run_vars_collection: JobRunVarCollection) -> bool:
        percentage = int(parameters.get("percentage", 50))
        logger.info(f"Chance result was {percentage}")
        return randint(0, 100) < percentage
