import click

from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.sast.sastbox import SASTBox
from convisoappsec.flow import GitAdapter
from convisoappsec.flowcli.common import project_code_option


def log_func(msg, new_line=True, clear=False):
    click.echo(msg, nl=new_line, err=True)


@click.command()
@project_code_option(
    required=False,
)
@click.option(
    '-s',
    '--start-commit',
    required=False,
    help="If no value is set so the empty tree hash commit is used."
)
@click.option(
    '-e',
    '--end-commit',
    required=False,
    help="""If no value is set so the HEAD commit
    from the current branch is used""",
)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    hidden=True,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required"""
)
@click.option(
    "--deploy-id",
    default=None,
    required=False,
    hidden=True,
    envvar="FLOW_DEPLOY_ID"
)
@click.option(
    "--sastbox-registry",
    default="",
    required=False,
    hidden=True,
    envvar="FLOW_SASTBOX_REGISTRY"
)
@click.option(
    "--sastbox-repository-name",
    default="",
    required=False,
    hidden=True,
    envvar="FLOW_SASTBOX_REPOSITORY_NAME"
)
@click.option(
    "--sastbox-tag",
    default=SASTBox.DEFAULT_TAG,
    required=False,
    hidden=True,
    envvar="FLOW_SASTBOX_TAG"
)
@click.option(
    "--sastbox-skip-login/--sastbox-no-skip-login",
    default=False,
    required=False,
    hidden=True,
    envvar="FLOW_SASTBOX_SKIP_LOGIN"
)
@help_option
@pass_flow_context
def run(
    flow_context, project_code, end_commit,
    start_commit, repository_dir, send_to_flow,
    deploy_id, sastbox_registry, sastbox_repository_name,
    sastbox_tag, sastbox_skip_login
):
    '''
      This command will perform SAST analysis at the source code. The analysis
      results can be reported or not to flow application. The analysis can be
      applied to specific commit range.

      This command will write the analysis reports files paths to stdout.
    '''
    perform_command(
        flow_context,
        project_code,
        end_commit,
        start_commit,
        repository_dir,
        send_to_flow,
        deploy_id,
        sastbox_registry,
        sastbox_repository_name,
        sastbox_tag,
        sastbox_skip_login,
    )


def perform_command(
    flow_context, project_code, end_commit,
    start_commit, repository_dir, send_to_flow,
    deploy_id, sastbox_registry, sastbox_repository_name,
    sastbox_tag, sastbox_skip_login
):
    if send_to_flow and not project_code:
        raise click.MissingParameter(
            'It is required when sending reports to flow api.',
            param_type='option',
            param_hint='--project-code',
         )

    try:
        git_adapater = GitAdapter(repository_dir)

        end_commit = (
            end_commit or git_adapater.head_commit
        )

        start_commit = (
            start_commit or git_adapater.empty_repository_tree_commit
        )

        if start_commit == end_commit:
            click.echo(
                "Previous commit ({0}) and Current commit ({1}) are the same, nothing to do.".format(
                    start_commit, end_commit
                )
            )
            return

        flow = flow_context.create_flow_api_client()
        sastbox = SASTBox(
            registry=sastbox_registry,
            repository_name=sastbox_repository_name,
            tag=sastbox_tag,
        )

        if not sastbox_skip_login:
            log_func('Checking SASTBox authorization...')
            token = flow.docker_registry.get_sast_token()
            sastbox.login(token)

        pull_progress_bar = click.progressbar(
            length=sastbox.size,
            label='Performing SASTBox download...',
        )

        with pull_progress_bar as progressbar:
            for downloaded_chunk in sastbox.pull():
                progressbar.update(downloaded_chunk)

        log_func('Starting SASTBox scandiff...')

        reports = sastbox.run_scan_diff(
            repository_dir, end_commit, start_commit, log=log_func
        )

        log_func('SASTBox scandiff done')

        report_names = [
            str(r) for r in reports
        ]

        if send_to_flow:
            default_report_type = "sast"
            commit_refs = git_adapater.show_commit_refs(
                end_commit
            )

            report_names_ctx = click.progressbar(
                report_names,
                label="Sending SASTBox reports to flow application"
            )

            with report_names_ctx as reports:
                for report_name in reports:
                    report_file = open(report_name)

                    flow.findings.create(
                        project_code,
                        commit_refs,
                        report_file,
                        default_report_type=default_report_type,
                        deploy_id=deploy_id,
                    )

                    report_file.close()

        for r in report_names:
            click.echo(r)

    except Exception as e:
        raise click.ClickException(str(e)) from e


EPILOG = '''
Examples:

  \b
  1 - Reporting the results to flow api:
    1.1 - Running an analysis at all commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command}

    \b
    1.2 - Running an analysis at specific commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command} --start-commit "$(git rev-parse HEAD~5)" --end-commit "$(git rev-parse HEAD)"
'''  # noqa: E501

SHORT_HELP = "Perform SAST analysis"

command = 'flow sast run'
run.short_help = SHORT_HELP
run.epilog = EPILOG.format(
    command=command,
)
