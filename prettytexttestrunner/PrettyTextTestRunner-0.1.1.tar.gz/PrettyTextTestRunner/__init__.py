from sys import stdout as SYS_STDOUT
import time
import warnings
import traceback
from unittest import TextTestRunner, TestResult
from unittest.result import failfast
from unittest.util import strclass
from unittest.signals import registerResult

__name__ = "PrettyTextTestRunner"
__module__ = "PrettyTextTestRunner"
__author__ = "Rob MacKinnon <rome@villagertechnolgies.com>"
__license__ = "MIT"
__version__ = "0.1.1"

__doc__ = """
Example Usage:

from unittest import TestLoader, TestSuite
from PrettyTextTestRunner import PrettyTextTestRunner
import test_suite_file1
import test_suite_file2

testcase1 = TestLoader().loadTestsFromTestCase(test_suite_file1.testcase1)
testcase2 = TestLoader().loadTestsFromTestCase(test_suite_file2.testcase2)

suite = TestSuite([testcase1, testcase2])

runner = PrettyTextTestRunner()
runner.run(suite)
"""


from .textTable import TextTable

START = "\x1b["
END = ""
COLOR = {
    'BLACK' : "0;30m",
    'RED' : "0;31m",
    'GREEN' : "0;32m",
    'YELLOW' : "0;33m",
    'BLUE' : "0;34m",
    'PURPLE' : "0;35m",
    'CYAN' : "0;36m",
    'WHITE' : "0;37m",
    'END' : "0m",
}

SETTING_USE_COLOR = True


class PrettyTestResult(TestResult):
    """ @abstract Extension class for TestResult, overriding output and forcing
            buffering. This is a drop-in replacement.
        @methods testName, testClsName, getClassTally, getResultTally
    """
    STATUS = {
        '.': "PASS",
        'F': "FAILED",
        'E': "ERROR",
        'S': "SKIP",
        '?': "SUCCESS?",
        'X': "EXPECTED"
    }

    def __init__(self, stream, descriptions, verbosity):
        self.timing = False
        self.results = {}
        self.tally = {}
        self.success_count = 0
        self.err_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.unexpectedSuccess_count = 0
        self.expectedFailure_count = 0
        self.execTimes = {}
        super(PrettyTestResult, self).__init__(stream, descriptions, verbosity)

    def testName(self, test):
        return test._testMethodName

    def testClsName(self, test):
        return ".".join(test.id().rsplit('.')[0:2])

    def getClassTally(self, clsName):
        _fieldOrder = [
            "success", "failed", "error", "skipped",
            "unexpectedSuccess", "expectedFail"
        ]
        return [str(self.tally[clsName][_v]) for _v in _fieldOrder]

    def getResultTally(self):
        _total_count = _total_success = _total_fail = _total_err = 0
        _total_skip = _total_unexpS = _total_expectF = 0

        for _clsName in self.tally:
            # "Count", "Pass", "Fail", "Error", "Skip", "UnexpS", "ExpectF"],
            _total_count += sum(self.tally[_clsName].values())
            _total_success += self.tally[_clsName]['success']
            _total_err += self.tally[_clsName]['error']
            _total_fail += self.tally[_clsName]['failed']
            _total_skip += self.tally[_clsName]['skipped']
            _total_unexpS += self.tally[_clsName]['unexpectedSuccess']
            _total_expectF += self.tally[_clsName]['expectedFail']

        return [
            str(_total_count), str(_total_success),
            str(_total_fail), str(_total_err),
            str(_total_skip), str(_total_unexpS),
            str(_total_expectF)
        ]

    def startTest(self, test):
        _clsName = self.testClsName(test)
        if _clsName not in self.results:
            self.results[_clsName] = []

        if _clsName not in self.tally:
            self.tally[_clsName] = {
                'success': 0,
                "error": 0,
                "failed": 0,
                "skipped": 0,
                "unexpectedSuccess": 0,
                "expectedFail": 0
            }

        if self.timing:
            testKey = test.id()
            start = time.time()
            self.execTimes.update({testKey: {'start': start}})
        super(PrettyTestResult, self).startTest(test)

    def stopTest(self, test):
        super(PrettyTestResult, self).stopTest(test)
        if self.timing:
            testKey = test.id()
            stop = time.time()
            self.execTimes[testKey].update({'stop': stop})

    def addSuccess(self, test):
        _clsName = self.testClsName(test)
        self.tally[_clsName]["success"] += 1
        self.results[_clsName].append((self.testName(test), test, '.', 
                                       self._exc_info_to_string((None,0,None), test)))
        super(PrettyTestResult, self).addSuccess(test)

    @failfast
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        _clsName = self.testClsName(test)
        self.tally[_clsName]["error"] += 1
        self.results[_clsName].append((self.testName(test), test, 'E', 
                                       self._exc_info_to_string(err, test)))
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = False

    @failfast
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        _clsName = self.testClsName(test)
        self.tally[_clsName]["failed"] += 1
        self.results[_clsName].append((self.testName(test), test, 'F', 
                                       self._exc_info_to_string(err, test)))
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = False

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().
        """
        # By default, we don't do anything with successful subtests, but
        # more sophisticated test results might want to record them.
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                errors = self.failures
            else:
                errors = self.errors
            errors.append((subtest, self._exc_info_to_string(err, test)))
            self._mirrorOutput = False

    def addSkip(self, test, reason):
        _clsName = self.testClsName(test)
        self.tally[_clsName]["skipped"] += 1
        self.results[_clsName].append((self.testName(test), test, 'S', 
                                       self._exc_info_to_string(err, test)))
        super(PrettyTestResult, self).addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        _clsName = self.testClsName(test)
        self.tally[_clsName]["expectedFail"] += 1
        self.results[_clsName].append((self.testName(test), test, 'X', 
                                       self._exc_info_to_string(err, test)))
        super(PrettyTestResult, self).addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        _clsName = self.testClsName(test)
        self.tally[_clsName]["unexpectedSuccess"] += 1
        self.results[_clsName].append((self.testName(test), test, '?', 
                                       self._exc_info_to_string((None,0,None), test)))
        super(PrettyTestResult, self).addUnexpectedSuccess(test)

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
        else:
            length = None

        msgLines = []
        if tb is not None:
            tb_e = traceback.TracebackException(
                exctype, value, tb, limit=length, capture_locals=self.tb_locals)
            msgLines = list(tb_e.format())

        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error)

        return ''.join(msgLines)


class PrettyTextTestRunner(TextTestRunner):
    """ @abstract Extension class for TextTestResult, overriding output and
            giving us some nice results to read and look at. This is a drop-in
            replacement for TextTestRunner.
        @methods run, setProps
        @props mode [str] "full-report" or "simple", defaults to full
        @props timing [bool] Display timing stats for tests
    """
    _summary_props = {
        "titles": [
            "Test Suite/Test Case",
            "Count", "Pass", "Fail", "Error", "Skip", "Unexp Sucess", "ExpectFails"],
        "colWidths": [30, 7, 7, 7, 7, 7, 8, 8],
        "colJustify": ["left", "center", "center", "center", "center",
                       "center", "center", "center"],
        "padding": 1,
        "indent": 0,
        "margins": {"top":0, "bottom": 0, "left": 0, "right": 0},
        "border": "solid"
    }

    _test_props = {
        "titles": ["Test Name", "Output", "Status"],
        "colWidths": [30, 50, 18],
        "colJustify": ["left", "left", "right"],
        "padding": 1,
        "indent": 5,
        "margins": {"top":0, "bottom": 1, "left": 0, "right": 0},
        "border": "solid"
    }

    def __init__(self, stream=SYS_STDOUT, descriptions=1, verbosity=0):
        self.buffer = True
        self.timing = True
        self.mode = "full-report"  # set to `simple` for micro report
        super(PrettyTextTestRunner, self).__init__(stream,
                                                   descriptions,
                                                   verbosity,
                                                   resultclass=PrettyTestResult)

    def setProps(self, summary: dict, testReport: dict):
        """ @abstract Change report formatting
            @params summary [dict] Description of summary table
            @params testReport [dict] Description of test report table, this
                applies to each test report
            @example Table Descriptor Format
                see [TextTable] for example
        """
        self._summary_props = summary
        self._test_props = testReport

    def run(self, test: object) -> TestResult: 
        """ @abstract Run the test suite or case and display the report
            @params test [TestSuite|TestCase] Test suite or case object to run
            @returns [TestResult] Outputs formatted text report and returns
                a TestResult object on success.
        """
        result = self._makeResult()
        registerResult(result)
        result.timing = self.timing
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals

        timetaken = 0
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                            category=DeprecationWarning,
                            message=r'Please use assert\w+ instead.')

            #overall testruntime
            startTime = time.time()

            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            stopTime = time.time()
            timeTaken = stopTime - startTime

        # We need to start building the report to display
        _reportOrder = result.tally.keys()
        if self.mode == "full-report":
            _summary_table = TextTable(self._summary_props)
            _total_count = _total_success = _total_fail = _total_err = 0
            _total_skip = _total_unexpS = _total_expectF = 0

            for _clsName in _reportOrder:
                # "Count", "Pass", "Fail", "Error", "Skip", "UnexpS", "ExpectF"],
                _test_count = sum(result.tally[_clsName].values())
                _summary_table.appendRow([_clsName, str(_test_count),
                                          *result.getClassTally(_clsName)])

        _resultTotals = result.getResultTally()
        _stats = ""

        if self.mode == "full-report":
            _summary_table.appendRow(["Totals", *_resultTotals])

            _reports = [("Summary", _summary_table)]

        for _cls in _reportOrder:
            _clsSet = result.results[_cls]
            if self.mode == "full-report":
                _report = TextTable(self._test_props)

            _single = len(_clsSet) == 1
            for _name, _test, _status, _output in _clsSet:
                if self.mode == "full-report":
                    if self.timing:
                        _execTimes = result.execTimes[_test.id()]
                        _runTime = round(_execTimes["stop"] - _execTimes["start"], 3)
                        _statStr = "({}s) {}".format(_runTime, result.STATUS[_status])
                    else:
                        _statStr = "{}".format(result.STATUS[_status])

                    _report.appendRow(cells=[_name, _output, _statStr], single=_single)
                else:
                    _stats += _status

            if self.mode == "full-report":
                _reports.append((_cls, _report))

        if self.mode == "full-report":
            for _heading, _report in _reports:
                print(_heading)
                _report.draw()
            if self.timing:
               print("runtime: {}s".format(round(timeTaken, 3)))
        else:
            _stats += " " if len(_stats) > 0 else ""

            # Simple Summary
            simplereport = "{}pass: {}, failed: {}, errors: {}, runtime: {}s" 
            print(simplereport.format(_stats, _resultTotals[1], _resultTotals[3],
                                      _resultTotals[2], round(timeTaken, 3)))
        return result

