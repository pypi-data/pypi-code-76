import argparse
from pathlib import Path
from typing import Iterable

from curricula_grade.models import GradingAssignment
from curricula_grade.shell import path_from_options, change_extension
from curricula.shell.plugin import Plugin, PluginException
from curricula.log import log


class FormatPlugin(Plugin):
    """Used for formatting reports as Markdown."""

    name = "format"
    help = "Format a graded report as Markdown"

    @classmethod
    def setup(cls, parser: argparse.ArgumentParser):
        """Set up the parser."""

        to_group = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument("--grading", "-g", required=True, help="the grading artifact")
        to_group.add_argument("-f", "--file", dest="file", help="formatted output file for single report")
        to_group.add_argument("-d", "--directory", dest="directory", help="where to write formatted reports if batched")
        parser.add_argument("-t", "--template", help="the markdown template for the report")
        parser.add_argument("reports", nargs="+", help="a variable number of reports to format")

    @classmethod
    def main(cls, parser: argparse.ArgumentParser, options: dict):
        """Format a bunch of reports."""

        grading_path: Path = Path(options["grading"]).absolute()
        if not grading_path.is_dir():
            raise PluginException("grading artifact does not exist!")

        from . import create_format_environment

        assignment = GradingAssignment.read(grading_path)
        custom_template_path = Path(options.get("template") or grading_path.joinpath("report.md"))
        environment = create_format_environment(custom_template_path=custom_template_path)

        if len(options["reports"]) == 1:
            log.debug(f"formatting report with template {custom_template_path}")
            report_path = Path(options.get("reports")[0])
            cls.format_single(assignment, report_path, environment, options)
        else:
            log.debug(f"formatting reports with template {custom_template_path}")
            cls.format_batch(assignment, map(Path, options.get("reports")), environment, options)

    @classmethod
    def format_single(
            cls,
            assignment: GradingAssignment,
            report_path: Path,
            environment,
            options: dict):
        """Format a single report."""

        from curricula_format import format_report_markdown
        output_path = path_from_options(options, change_extension(report_path, "md"), batch=False, required=False)
        formatted_report = format_report_markdown(
            assignment=assignment,
            report_path=report_path,
            environment=environment,
            options=options)
        if output_path is not None:
            with output_path.open("w") as file:
                file.write(formatted_report)
        else:
            print(formatted_report)

    @classmethod
    def format_batch(cls, assignment: GradingAssignment, report_paths: Iterable[Path], environment, options: dict):
        """Format a batch of results."""

        for report_path in report_paths:
            cls.format_single(assignment, report_path, environment, options)


