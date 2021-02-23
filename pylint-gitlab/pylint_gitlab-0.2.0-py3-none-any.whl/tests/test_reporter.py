#
# Copyright 2019 Stephan Müller
#
# Licensed under the MIT license

"""Tests for ``pylint_gitlab.reporter``."""

import json
import os
from io import StringIO

from pylint import checkers
from pylint.lint import PyLinter

from pylint_gitlab.reporter import GitlabCodeClimateReporter, GitlabPagesHtmlReporter


def test_gitlab_pages_html_reporter():
    """Tests for ``pylint_gitlab.reporter.GitlabPagesHtmlReporter()``."""

    output = StringIO()

    reporter = GitlabPagesHtmlReporter()
    reporter.CI_PROJECT_URL = "https://example.org"
    reporter.CI_COMMIT_REF_NAME = "branch"
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)

    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.open()

    linter.set_current_module("b")
    linter.add_message("line-too-long", line=2, args=(1, 2))
    linter.add_message("line-too-long", line=1, args=(1, 2))

    linter.set_current_module("a")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.html"), "r") as file:
        expected_result = file.read()
    assert output.getvalue() == expected_result


def test_gitlab_code_climate_reporter():
    """Tests for ``pylint_gitlab.reporter.GitlabCodeClimateReporter()``."""

    output = StringIO()

    reporter = GitlabCodeClimateReporter()
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)

    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    expected_result = [{
        "description": "C0301: Line too long (1/2)",
        "severity": "minor",
        "location": {
            "path": "0123",
            "lines": {
                "begin": 1,
            }
        },
        "fingerprint": "21e7b7887a841a99f73b9cf1771bf387"
    }]
    report_result = json.loads(output.getvalue())
    assert report_result == expected_result
