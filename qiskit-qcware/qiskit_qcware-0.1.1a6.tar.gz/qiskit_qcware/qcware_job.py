from qiskit.providers import (JobV1, JobError, JobTimeoutError, Backend,
                              JobStatus)
from qiskit.result import Result
from icontract import require
from typing import Optional

# using base from https://github.com/Qiskit/qiskit-terra/blob/master/qiskit/providers/job.py


class QcwareJob(JobV1):

    # The documentation says the job "allows to synchronize different executions of the simulator",
    # but this is not completely clear.
    # https://qiskit.org/documentation/stubs/qiskit.providers.BaseJob.html?highlight=basejob#qiskit.providers.BaseJob
    # job_id(str) is "a unique id in the context of the backend used to run the job
    def __init__(self, backend: Backend, job_id: str, **kwargs) -> None:
        super().__init__(backend, job_id, **kwargs)
        self._result: Optional[Result] = None
        self._status = JobStatus.INITIALIZING

    @require(lambda self: self.in_final_state())
    def result(self) -> Result:
        """
        Return the results of the job.
        """
        # can wait for the result here (AQT does this)
        # but the intent is to be asynchronous
        return self._result

    def cancel(self):
        """
        Attempt to cancel the job (NOP for local simulator,
        raises NotImplementedError)
        """
        super().cancel()

    def status(self) -> JobStatus:
        """
        Return the status of the job, among the values of JobStatus
        """
        # see qiskit.providers.jobstatus
        # https://github.com/Qiskit/qiskit-terra/blob/900c048df8d763ec1b43cb0d32afb3e6ef5c48ae/qiskit/providers/jobstatus.py
        return self._status

    def submit(self):
        """
        Submit the job to the backend for execution.  Deprecated; the backend should
        be handling the submission
        """
        raise NotImplementedError
