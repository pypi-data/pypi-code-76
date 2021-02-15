from math import ceil
import sys
from typing import Tuple

import click
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
from gitlab.v4.objects import Issue

from boiler import BOILER_CONFIG_FILE, cli, get_config_value


ISSUE_TEMPLATE = """
AUDITOR:

DATE AUDIT COMPLETE: MM/DD/YY

* Number of Janitor Tasks: {tasks}
* Number of Janitor Tasks to 95% complete: {to_95}

Project to charge (with KWIK ID): IARPA DIVA-Option 2-Annotation Generation K002093-00-T27

Path to janitor task: <http://admin.stumpf.avidannotations.com/#/tasks?video={video_name}>


**Notes:** You will need to correct or approve the annotations for the janitor activities
associated with this clip. You should *not* review the entire clip.
"""  # noqa

TITLE_TEMPLATE = 'DIVA M2 Janitor {video_name}'  # noqa


@click.group(name='janitor')
@click.pass_obj
def janitor(ctx):
    try:
        ctx['kwgitlab'] = gitlab.Gitlab(
            ctx['gitlab_url'],
            timeout=10,
            private_token=get_config_value(BOILER_CONFIG_FILE, 'kwgitlab_token'),
        )
        ctx['kwgitlab'].auth()
        ctx['kwgitlab_project'] = ctx['kwgitlab'].projects.get(ctx['gitlab_project_id'])
    except GitlabAuthenticationError:
        click.echo(
            click.style(
                "You are attempting to perform an authorized operation but you aren't authenticated with kwgitlab.\n"  # noqa
                'Run the following command: boiler login kwgitlab',
                fg='yellow',
            ),
            err=True,
        )
        sys.exit(1)


def _create_or_reopen_issue(ctx, video_name, tasks, activities, **kwargs) -> Tuple[Issue, bool]:
    # TODO: how to handle if there's more than one issue
    existing_issue = ctx['kwgitlab_project'].search(
        'issues', TITLE_TEMPLATE.format(video_name=video_name)
    )

    if existing_issue:
        existing_issue = ctx['kwgitlab_project'].issues.get(existing_issue[0]['iid'])

        if existing_issue.state == 'closed':
            existing_issue.state_event = 'reopen'
            existing_issue.save()
        return existing_issue, False

    to_95 = max(ceil(tasks - 0.05 * activities), 0)
    labels = ['DIVA', 'Janitor', 'Unassigned']
    if to_95 > 0:
        labels.append('High')
    else:
        labels.append('Medium')

    issue = ctx['kwgitlab_project'].issues.create(
        {
            'title': TITLE_TEMPLATE.format(video_name=video_name),
            'description': ISSUE_TEMPLATE.format(
                video_name=video_name, activities=activities, tasks=tasks, to_95=to_95,
            ),
            'labels': labels,
        },
        retry_transient_errors=True,
    )
    return issue, True


def _maybe_create_video_issue_association(ctx, video_id, issue_url):
    r = ctx['session'].post('task/issue', json={'video_id': video_id, 'issue_url': issue_url})

    # ignore conflict errors
    if not r.ok and r.status_code != 409:
        r.raise_for_status()


@janitor.command(name='create-issues')
@click.pass_obj
def create_issues(ctx):
    r = ctx['session'].get('video-pipeline/gunrunner/pending-janitor-tasks')
    for pending_task in r.json():
        issue, created = _create_or_reopen_issue(ctx, **pending_task)

        _maybe_create_video_issue_association(ctx, pending_task['video_id'], issue.web_url)

        if created:
            click.echo(f'created issue  {issue.iid:5}: {issue.web_url}')
        else:
            click.echo(f'reopened issue {issue.iid:5}: {issue.web_url}')


cli.add_command(janitor)
