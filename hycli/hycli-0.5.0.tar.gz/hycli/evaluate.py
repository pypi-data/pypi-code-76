import csv
import json
from pathlib import Path

import click
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from hycli.evaluation.evaluation import Evaluation, Granularity
from hycli.commands.context_default import CONTEXT_SETTINGS


def check_required_options(ctx, param, value):
    if value is None:
        if not ctx.obj.get('ground_truth_file'):
            set_option_as_required(ctx, 'ground_truth_file')
        if not ctx.obj.get('model_1_file'):
            set_option_as_required(ctx, 'model_1_file')
        if not ctx.obj.get('model_2_file'):
            set_option_as_required(ctx, 'model_2_file')
    return value


def set_option_as_required(ctx, name):
    for p in ctx.command.params:
        if isinstance(p, click.Option) and p.name == name:
            p.required = True


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--job-id",
    default=None,
    help='Definition: The ID for the evaluation in format "%Y%m%d_%H%M%S".\n'
         "Instruction: Only enter job_id if you want to get a report from a previous job.\n"
         "Leave it empty if running a report for the first time.",
    callback=check_required_options
)
@click.option(
    "--ground-truth-file",
    "-gt",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the ground truth file.\n"
         "Instruction: Only enter ground_truth_file if you want to create a new report.\n"
         "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--model-1-file",
    "-m1",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the model 1 extractions.\n"
         "Instruction: Only enter model_1_file if you want to create a new report.\n"
         "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--model-2-file",
    "-m2",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the model 2 extractions.\n"
         "Instruction: Only enter model_2_file if you want to create a new report.\n"
         "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--entities",
    "-e",
    default=None,
    help="Definition: Entity that will be used for model evaluation.\n"
         "Accepts multiple values",
    multiple=True,
)
@click.option(
    "--vendor-field",
    "-v",
    default=None,
    help="Definition: Column name for the vendor id.\n"
         "Instruction: Only enter vendor_field if you want to create a vendor report.\n"
         "Leave it empty if you are not interested in a vendor performance report.",
)
@click.option(
    "--report-dir",
    "-d",
    default=Path.cwd() / "report",
    type=click.Path(),
    help="Definition: directory of the report files.\n"
         "Default: A report directory will be created under current directory",
)
@click.option(
    "--report-format",
    "-f",
    default="csv",
    type=click.Choice(["json", "csv"]),
    help="Definition: output format for your report.\n" "Options: json, csv",
)
@click.pass_context
def evaluate(
        ctx,
        job_id,
        ground_truth_file,
        model_1_file,
        model_2_file,
        entities,
        vendor_field,
        report_dir,
        report_format,
):
    """Evaluate two models' performance against ground truth. """
    ctx.ensure_object(dict)

    ctx.obj["job_id"] = job_id
    ctx.obj["ground_truth_file"] = ground_truth_file

    ctx.obj["model_1_file"] = model_1_file
    ctx.obj["model_2_file"] = model_2_file
    ctx.obj["entities"] = set(entities) or None
    ctx.obj["vendor_field"] = vendor_field
    ctx.obj["report_dir"] = report_dir
    ctx.obj["report_format"] = report_format


@click.command()
@click.pass_context
def create_report(ctx):
    """Create an accuracy report for model extraction results. """

    sns.set_theme(style="whitegrid")

    evaluation = Evaluation(
        job_id=ctx.obj["job_id"],
        ground_truth_file=ctx.obj["ground_truth_file"],
        model_1_file=ctx.obj["model_1_file"],
        model_2_file=ctx.obj["model_2_file"],
        entities=ctx.obj["entities"],
        vendor_field=ctx.obj["vendor_field"],
    )
    output_dir = Path(ctx.obj["report_dir"]) / evaluation.job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    all_reports = {}

    model_report = evaluation.create_report(granularity=Granularity.MODEL)
    all_reports["model"] = model_report
    model_df = pd.DataFrame(data=model_report)
    sns.barplot(x="model_id", y="accuracy", data=model_df)
    plt.xticks(fontsize="x-small")
    plt.savefig(output_dir / "model", bbox_inches='tight')
    plt.clf()

    entity_report = evaluation.create_report(granularity=Granularity.ENTITY)
    all_reports["entity"] = entity_report
    entity_df = pd.DataFrame(data=entity_report)[:20]
    sns.barplot(y="entity", x="accuracy", hue="model_id", data=entity_df, orient='h')
    plt.yticks(fontsize="x-small")
    plt.legend(bbox_to_anchor=(0, 1.1), loc="upper left", fontsize="x-small")
    plt.savefig(output_dir / "entity", bbox_inches='tight')
    plt.clf()

    if ctx.obj["vendor_field"]:
        vendor_report = evaluation.create_report(granularity=Granularity.VENDOR)
        all_reports["vendor"] = vendor_report

    for report_name, data in all_reports.items():
        if ctx.obj["report_format"] == "json":
            with open(output_dir / f"{report_name}.json", "w") as fp:
                json.dump(data, fp)
        elif ctx.obj["report_format"] == "csv":
            _dict_to_csv(data, output_dir / f"{report_name}.csv")

    print(f"Created report in {output_dir}")


def _dict_to_csv(data, report_path):
    with open(report_path, "w") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


evaluate.add_command(create_report)

if __name__ == "__main__":
    evaluate(obj={})
