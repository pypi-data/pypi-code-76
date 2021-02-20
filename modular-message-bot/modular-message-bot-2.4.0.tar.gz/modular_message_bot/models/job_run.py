from dataclasses import dataclass
from typing import Any, Dict, List

from modular_message_bot.string_interpolator import StringInterpolator


@dataclass
class JobRunVar(object):
    code: str
    value: Any
    # List of input codes that interpolated the value above
    interpolated_by_input_codes: list

    def add_interpolated_by_input_codes(self, input_code: str):
        if input_code not in self.interpolated_by_input_codes:
            self.interpolated_by_input_codes.append(input_code)


class JobRunVarCollection(object):
    def __init__(self, job_var_interpolator: StringInterpolator, job_run_vars: list = None):
        self.job_var_interpolator = job_var_interpolator
        self.job_run_vars: List[JobRunVar] = []
        self.job_run_vars_by_code: Dict[str, JobRunVar] = {}
        if job_run_vars is not None:
            for job_run_var in job_run_vars:
                self.add_job_run_var(job_run_var)

    def add_job_run_var(self, job_run_var: JobRunVar):
        self.job_run_vars.append(job_run_var)
        self.job_run_vars_by_code[job_run_var.code] = job_run_var

    def get_all(self) -> List[JobRunVar]:
        return self.job_run_vars

    def get_by_code(self, var: str) -> Any:
        return self.job_run_vars_by_code[var] or None

    def interpolate(self, key: str, value: str, job_input_code: str = None):
        job_run_var: JobRunVar
        for job_run_var in self.job_run_vars:
            if not isinstance(job_run_var.value, str):
                continue
            if self.job_var_interpolator.is_interpolatable(job_run_var.value, key):
                job_run_var.value = self.job_var_interpolator.interpolate(job_run_var.value, key, value)
                if job_input_code is not None:
                    job_run_var.add_interpolated_by_input_codes(job_input_code)

    def interpolate_into_parameters(self, parameters: dict):
        job_var: JobRunVar
        for job_var in self.job_run_vars:
            if isinstance(job_var.value, str):
                parameters = self.job_var_interpolator.interpolate_dict(parameters, job_var.code, job_var.value)
        return parameters
