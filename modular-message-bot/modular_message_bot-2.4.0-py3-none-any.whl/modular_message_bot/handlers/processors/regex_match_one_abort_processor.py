"""
# Regex Match One Abort
Abort job if we match one of the regexes

```yaml
- code: regex_match_one_abort
  parameters:
     match:
        weather_edi: clouds
        weather_gla: clouds
```
"""
import logging

from modular_message_bot.handlers.processors.abstract_regex_match_handler import AbstractRegexMatchProcessor
from modular_message_bot.models.job_run import JobRunVarCollection

logger = logging.getLogger(__name__)


class RegexMatchOneAbortProcessor(AbstractRegexMatchProcessor):
    @classmethod
    def get_code(cls) -> str:
        return "regex_match_one_abort"

    def process(self, parameters: dict, job_run_vars_collection: JobRunVarCollection) -> bool:
        results = self.get_match_results(parameters, job_run_vars_collection)

        if True in results:
            logger.info(f"Aborting job due to {self.get_code()}")
            return False  # Abort job

        # Else its ok
        return True  # Do not abort
