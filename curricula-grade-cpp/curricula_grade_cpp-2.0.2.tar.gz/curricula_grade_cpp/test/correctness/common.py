from curricula_grade.common.process import ProcessExecutor, ProcessExitCodeConnector
from curricula_grade.test.correctness.common import CorrectnessRunnable, CompareExitCodeEvaluator


class GoogleTest(ProcessExecutor, ProcessExitCodeConnector, CompareExitCodeEvaluator, CorrectnessRunnable):
    """Is set up for the gtest.hpp include."""

    expected_code = 0

    def __init__(self, test_name: str, *args, **kwargs):
        """Relies on the harness in """

        super().__init__(*args, **kwargs)
        self.args = (test_name,)
