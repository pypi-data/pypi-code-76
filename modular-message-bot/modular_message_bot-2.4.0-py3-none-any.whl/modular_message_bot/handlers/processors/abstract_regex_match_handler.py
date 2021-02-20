"""
# Abstract Regex Match Abort
Class to handle the duplicate logic between all the regex match handlers
"""
import re
from abc import ABC

from modular_message_bot.handlers.processors.abstract_processor_handler import AbstractProcessorHandler
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection


class AbstractRegexMatchProcessor(AbstractProcessorHandler, ABC):
    @classmethod
    def get_match_results(cls, parameters: dict, job_run_vars_collection: JobRunVarCollection) -> list:
        match = parameters.get("match", {})

        # Check each Regex
        results = []
        for var, regex_pattern in match.items():
            job_run_var: JobRunVar = job_run_vars_collection.get_by_code(var)
            matches = re.search(regex_pattern, str(job_run_var.value))
            has_matches = matches is not None
            results.append(has_matches)

        return results
