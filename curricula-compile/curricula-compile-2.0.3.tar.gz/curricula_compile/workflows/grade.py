import json

from ..models import CompilationAssignment
from ..framework import Workflow, TargetResult
from curricula.structure import Paths


class GradeWorkflow(Workflow):
    """Grades the solution and writes the report to the artifact root."""

    def run(self, assignment: CompilationAssignment, result: TargetResult):
        """Main."""

        if not self.configuration.options.get("grade"):
            return

        if not result["grading"].compiled and not result["solution"].compiled:
            return

        from curricula_grade.run import run
        from curricula_grade.models import GradingAssignment
        # from curricula_grade.tools.format import format_report_markdown
        from curricula_grade.tools.diagnose import diagnose

        grading_path = self.configuration.artifacts_path.joinpath(Paths.GRADING)
        solution_path = self.configuration.artifacts_path.joinpath(Paths.SOLUTION)
        report_path = self.configuration.artifacts_path.joinpath("solution.report.json")
        formatted_report_path = self.configuration.artifacts_path.joinpath("solution.report.md")

        assignment = GradingAssignment.read(grading_path)
        report = run(assignment, solution_path, options=self.configuration.options)

        with report_path.open("w") as file:
            json.dump(report.dump(), file, indent=2)

        # with formatted_report_path.open("w") as file:
        #     file.write(format_report_markdown(
        #         assignment=assignment,
        #         report_path=report_path,
        #         options=self.configuration.options))

        print(diagnose(assignment, report_path), end="")
