#!/usr/bin/env python3
import argparse
import datetime
import logging
import os
import sys
from urllib.parse import quote

import dateutil.parser
import requests


class GitlabApi:
    def __init__(self, server, project_id, auth):
        self.logger = logging.getLogger(__name__)
        self.server = server
        self.project_id = project_id
        self.auth = auth

    def make_request(self, request_url) -> dict:
        try:
            response = requests.get(
                request_url,
                headers=self.auth,
                verify=True,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            self.logger.error(f'Call to GitLab API failed with HTTPError: {ex}')
            sys.exit(1)
        except requests.exceptions.ConnectionError as ex:
            self.logger.error(f'Call to GitLab API failed with ConnectionError: {ex}')
            sys.exit(1)

        self.logger.debug(response.status_code)
        self.logger.debug(response.json())

        return response.json()

    def get_releases_for_project(self) -> dict:
        request_url = f'{self.server}/api/v4/projects/{self.project_id}/releases'
        return self.make_request(request_url)

    def get_tags_for_project(self) -> dict:
        request_url = f'{self.server}/api/v4/projects/{self.project_id}/repository/tags'
        return self.make_request(request_url)

    def get_closed_issues_for_project(self, updated_before, updated_after) -> dict:
        request_url = f'{self.server}/api/v4/projects/{self.project_id}' \
                      f'/issues?state=closed&updated_before={updated_before}&updated_after={updated_after}'
        return self.make_request(request_url)

    def get_merged_merge_requests_for_project(self, updated_before, updated_after) -> dict:
        request_url = f'{self.server}/api/v4/projects/{self.project_id}' \
                      f'/merge_requests?state=merged&updated_before={updated_before}&updated_after={updated_after}'
        return self.make_request(request_url)


def create_markdown(date, issues, merge_requests):
    header = f'### Release note ({date})\r\n\r\n'

    issue_header = f'#### Closed issues\r\n'
    issues_content = []
    if len(issues) > 0:
        issues_content = [f'- {issue["title"]} [(#{issue["iid"]})]({issue["web_url"]})\r\n' for issue in issues]

    merge_request_header = f'#### Merged merge requests\r\n'
    merge_request_content = []

    if len(merge_requests) > 0:
        for merge_request in merge_requests:
            assignee = merge_request['assignee']
            title = f'- {merge_request["title"]} [(#{merge_request["iid"]})]({merge_request["web_url"]})'
            if assignee is not None:
                title += f' ([{assignee["username"]}]({assignee["web_url"]}))\r\n'
            else:
                title += '\r\n'
            merge_request_content.append(title)

    notes = header + issue_header + ''.join(issues_content
                                            ) + '\r\n' + merge_request_header + ''.join(merge_request_content)
    return notes


def create_release_notes(server, project_id, auth):
    gitlab_api = GitlabApi(server, project_id, auth)
    tags = gitlab_api.get_tags_for_project()
    try:
        updated_before = tags[0]['commit']['committed_date']
        updated_before = dateutil.parser.parse(updated_before) + datetime.timedelta(0, 2)
        updated_before = updated_before.isoformat()
    except Exception as e:
        logger.error(str(e))
        exit(-1)
    try:
        updated_after = tags[1]['commit']['committed_date']  # replace with
        updated_after = dateutil.parser.parse(updated_after) + datetime.timedelta(0, 2)
        updated_after = updated_after.isoformat()
    except IndexError:
        updated_after = datetime.datetime(1970, 1, 1).isoformat()
    committed_date = dateutil.parser.parse(tags[0]['commit']['committed_date'])
    formatted_date = committed_date.strftime('%Y-%m-%d %H:%M:%S')
    closed_issues = gitlab_api.get_closed_issues_for_project(updated_before, updated_after)
    merged_merge_requests = gitlab_api.get_merged_merge_requests_for_project(updated_before, updated_after)
    notes = create_markdown(formatted_date, closed_issues, merged_merge_requests)
    return notes


def main():
    parser = argparse.ArgumentParser(description='Generate release notes.')
    parser.add_argument(
        '--server', default=os.environ.get('CI_PROJECT_URL'), help='Url of gitlab server (default: $CI_PROJECT_URL)'
    )
    parser.add_argument(
        '--project-id',
        default=os.environ.get('CI_PROJECT_ID'),
        help='Unique id of project, available in Project Settings/General (default: $CI_PROJECT_ID)'
    )
    parser.add_argument(
        '--private-token',
        default=os.environ.get('PRIVATE_TOKEN'),
        help='login token with permissions to commit to repo. (default: $PRIVATE_TOKEN)'
    )

    parser.add_argument(
        '--file',
        type=argparse.FileType('w+'),
        default=sys.stdout,
        help='The changelog file which shall be written. (default: sys.stdout)'
    )

    args = parser.parse_args()

    server = args.server
    if not server:
        raise SystemExit('Must provide --server if not running from CI')
    if server.endswith('/'):
        server -= '/'

    project_id = args.project_id
    if not project_id:
        raise SystemExit('Must provide --project_id if not running from CI')
    project_id = quote(project_id, safe='')

    private_token = args.private_token
    if private_token:
        auth = {'PRIVATE-TOKEN': private_token}
    else:
        raise SystemExit("PRIVATE_TOKEN must be in env var 'PRIVATE_TOKEN' or provided as arg")
    try:
        notes = create_release_notes(server=server, project_id=project_id, auth=auth)
    except Exception as e:
        logger.error(str(e))
        raise

    with args.file as changelog:
        changelog.write(notes)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    main()
