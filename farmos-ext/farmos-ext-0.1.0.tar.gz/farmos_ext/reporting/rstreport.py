
from __future__ import annotations

from typing import Dict, List, Union

from farmos_ext.reporting.report import Report

TITLE = "="

HEADING = [
    TITLE,
    "=",
    "-",
    "^",
    "*"
]


class RstReporter(Report):

    def __init__(self, filename: str):
        self._doc = ""
        super().__init__(filename)
        self.title(self.filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    @staticmethod
    def _sanitize(text: str):
        cleaned = text.replace("<p>", "").replace("</p>", "").replace("&nbsp;", "\n").replace("\n\n", "\n").replace(
            "<br />", "\n\n").replace("<dl>", "\n").replace("</dl>", "\n").replace("<dd>", "\n\n").replace(
                "</dd>", "\n\n").replace("<dt>", "**").replace("</dt>", "**\n")
        return cleaned.replace("\n\n", "\n")

    def _append(self, text: str):
        self._doc += RstReporter._sanitize(text)

    def line(self, text=""):
        if text is not None:
            self._append("{}\n".format(text))

    def directive(self, name: Union[str, Dict[str, str]],
                  configs: Union[None, List[Union[str, Dict[str, str]]]]):
        self.line()
        if isinstance(name, str):
            self.line(".. {}::".format(name))
        elif isinstance(name, dict):
            for key in name:
                self.line(".. {}:: {}".format(key, name[key]))
        if configs:
            for config in configs:
                if isinstance(config, str):
                    self.line("    :{}:".format(config))
                elif isinstance(config, dict):
                    for key in config:
                        self.line("    :{}: {}".format(key, config[key]))
        self.line()

    def title(self, text: str):
        self.line(TITLE * len(text))
        self.line(text)
        self.line(TITLE * len(text))
        self.line()

    def heading(self, text: str, level: int):
        self.line()
        self.line(text)
        self.line(HEADING[level] * len(text))
        self.line()

    def lists(self, items: List[str], ordered=True):
        denote = "#" if ordered else "-"
        self.line()
        for item in items:
            self.line("{} {}".format(denote, item))
        self.line()

    def definition(self, key: str, term: str):
        self.line(":{}: {}".format(key, term))

    def toctree(self, depth=1):
        self.directive("contents", ["local", {"depth": depth}])

    def pagebreak(self):
        self.directive({"raw": "pdf"}, None)
        self.line("    PageBreak")
        self.line()

    def table(self, items: List[Dict]):
        def row(cols: List[str], widths: List[int]):
            new_list = []
            for index, col in enumerate(cols):
                new_list.append("{col:{width}}".format(
                    col=col, width=widths[index]))
            return "| {} |".format(" | ".join(new_list))

        def sep(widths: List[int]):
            self.line(
                "+{}+".format("+".join(["-"*(index+2) for index in widths])))

        keys = list(items[0].keys())
        col_widths = [0] * len(keys)
        for index, key in enumerate(keys):
            if len(key) > col_widths[index]:
                col_widths[index] = len(key)
            for item in items:
                if len(item[key]) > col_widths[index]:
                    col_widths[index] = len(item[key])
        header = row(keys, col_widths)
        sep(col_widths)
        self.line(header)
        sep(col_widths)

        for item in items:
            self.line(row([item[key] for key in keys], col_widths))
            sep(col_widths)

    def image(self, path):
        self.directive({'image': path}, None)

    def save(self):
        path = "{}.rst".format(self.filename) if not self.filename.endswith(
            ".rst") else self.filename
        with open(path, 'w', encoding='utf-8') as rst:
            rst.write(self._doc)
