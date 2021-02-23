#
# Copyright 2019 Stephan Müller
#
# Licensed under the MIT license

"""Gitlab codequality reporter"""
from __future__ import absolute_import, print_function

import hashlib
import html
import json
import os
import sys
from collections import OrderedDict
from itertools import groupby

from jinja2 import FileSystemLoader, Environment
from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter


class GitlabPagesHtmlReporter(BaseReporter):
    """Report messages in HTML document with links to GitLab source code."""

    __implements__ = IReporter
    name = "gitlab-pages-html"
    extension = "html"

    CI_PROJECT_URL = os.getenv("CI_PROJECT_URL", "")
    CI_COMMIT_REF_NAME = os.getenv("CI_COMMIT_REF_NAME", "")

    _MSG_TYPES = {
        "info": "table-primary",
        "convention": "table-primary",
        "refactor": "table-primary",
        "warning": "table-warning",
        "error": "table-error",
        "fatal": "table-error",
    }

    _COLUMN_NAMES = OrderedDict({
        "line": "Line",
        "column": "Column",
        "type": "Type",
        "obj": "Object",
        "message": "Message",
        "symbol": "Symbol",
        "message_id": "Message Id",
    })

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""
        self.messages.append(msg)

    def display_messages(self, layout):
        """Launch layouts display."""

        ordered_messages = OrderedDict()

        sorted_messages = sorted(self.messages, key=lambda msg: msg.module)
        for module, messages in groupby(sorted_messages, lambda msg: msg.module):
            ordered_messages.update({module: list()})
            for message in list(messages):
                ordered_messages[module].append({
                    "class": self._MSG_TYPES[message.category],
                    "url": self.CI_PROJECT_URL + "/blob/" + self.CI_COMMIT_REF_NAME + "/" + message.path + "#L" + str(
                        message.line),
                    "path": message.path,
                    "row": OrderedDict({
                        "line": message.line,
                        "column": message.column,
                        "type": message.category,
                        "obj": message.obj,
                        "message": message.msg.replace("\n", "<br />"),
                        "symbol": message.symbol,
                        "message_id": message.msg_id,
                    })
                })

        template = Environment(
            loader=FileSystemLoader(
                searchpath=os.path.dirname(os.path.abspath(__file__))
            )
        ).get_template("templates/report.html.j2")

        print(template.render(data=ordered_messages, column_names=self._COLUMN_NAMES), file=self.out)

    def display_reports(self, layout):
        """Do nothing."""

    def _display(self, layout):
        """Do nothing."""


class GitlabCodeClimateReporter(BaseReporter):
    """Report messages and layouts in Gitlab Code Climate format. Read more on
    https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html."""

    __implements__ = IReporter
    name = "gitlab-codeclimate"
    extension = "json"

    _MSG_TYPES = {
        "info": "info",
        "convention": "minor",
        "refactor": "major",
        "warning": "major",
        "error": "critical",
        "fatal": "blocker",
    }

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""
        self.messages.append({
            "description": html.escape(msg.msg_id + ': ' + msg.msg or "", quote=False),
            "severity": self._MSG_TYPES[msg.category],
            "location": {
                "path": msg.path,
                "lines": {
                    "begin": msg.line,
                }
            },
            "fingerprint": hashlib.md5(":".join([msg.path, str(msg.line), msg.msg_id]).encode()).hexdigest()
        })

    def display_messages(self, layout):
        """Launch layouts display."""
        print(json.dumps(self.messages, indent=4), file=self.out)

    def display_reports(self, layout):
        """Do nothing."""

    def _display(self, layout):
        """Do nothing."""
