import json
import os
import sys
import argparse
import logging

import requests
from requests.auth import HTTPBasicAuth


class BitBucketException(Exception):
    pass


class BitBucket:
    def __init__(self, user_name, password, team):
        self.base_url = 'https://api.bitbucket.org/2.0'
        self.team = team
        self.auth = HTTPBasicAuth(user_name, password)

    def create_pr(self, repo_slug, title, src_branch, dest_branch='master'):
        url = f'{self.base_url}/repositories/{self.team}/{repo_slug}/pullrequests'
        data = {
            'title': title,
            'source': {
                'branch': {
                    'name': src_branch
                }
            },
            'destination': {
                'branch': {
                    'name': dest_branch
                }
            }
        }
        resp = requests.post(url, auth=self.auth, json=data)
        if resp.status_code != 201:
            logging.error(f'{resp.status_code}: {resp.text}')
            raise BitBucketException(f'Error creating PR {title}, {src_branch} to {dest_branch}')
        return json

    def if_branch_in_prs(self, project_name, branch_name):
        # filter for branch name
        opened_prs = self._get_opened_pr(project_name)
        source_branches = [p.get('source').get('branch').get('name') for p in opened_prs]
        if branch_name in source_branches:
            return True

    def get_last_commit_author(self, repo_name, branch_name):
        commit_hash = self._get_branch_info(repo_name, branch_name)['target']['hash']
        return self._get_commit_info(repo_name, commit_hash)['author']['raw']

    def find_branches(self, repo_slug, branch_name):
        url = f'{self.base_url}/repositories/{self.team}/{repo_slug}/refs/branches'
        params = {
            #"q": f'name~"{branch_name}"'
            "q": f'name="{branch_name}"'
        }
        resp = requests.get(url, auth=self.auth, params=params)
        if resp.status_code == 200:
            return [item['name'] for item in resp.json()['values']]

    def create_branch(self, repo_slug, branch_name, target_hash='master'):
        url = f'{self.base_url}/repositories/{self.team}/{repo_slug}/refs/branches'
        data = {
            'name': branch_name,
            'target': {
                'hash': target_hash
            }
        }
        resp = requests.post(url, auth=self.auth, json=data)
        if resp.status_code != 201:
            logging.error(f'{resp.status_code}: {resp.text}')
            raise BitBucketException(f'Error creating branch {branch_name} for repo {repo_slug}')
        return resp.json()

    # недоделанный генератор, валится на последнем цикле
    def _branches_gen(self, repo_slug):
        next_url = f'{self.base_url}/repositories/{self.team}/{repo_slug}/refs/branches'
        has_next = True
        while has_next:
            resp = requests.get(next_url, auth=self.auth)
            if resp.status_code == 200:
                resp_values = resp.json()
                if 'next' not in resp_values:
                    has_next = False
                yield resp_values['values']
                next_url = resp_values['next']

    def start_custom_pipeline(self, repo_name, build_branch, pipeline_name, variables):
        data = {
            'target': {
                "type": "pipeline_ref_target",
                "ref_type": "branch",
                "ref_name": build_branch,
                "selector": {
                    "type": "custom",
                    "pattern": pipeline_name
                }
            },
        }
        if variables:
            data.update({'variables': variables})
        url = '{}/repositories/{}/{}/pipelines/'.format(self.base_url, self.team, repo_name)
        resp = requests.post(url, auth=self.auth, json=data)
        if resp.status_code != 201:
            raise BitBucketException(f'failed to start pipeline: {resp.text}')
        return resp.json()

    def _get_opened_pr(self, project):
        url = f'{self.base_url}/repositories/{self.team}/{project}/pullrequests?q=state="open"'
        resp = requests.get(url, auth=self.auth)
        if resp.status_code == 200:
            return resp.json()['values']

    def _get_branch_info(self, repo_name, branch_name):
        url = '{}/repositories/{}/{}/refs/branches/{}'.format(
            self.base_url, self.team,
            repo_name, branch_name
        )
        req = requests.get(url, auth=self.auth)
        return req.json()

    def _get_commit_info(self, repo_name, commit_hash):
        url = '{}/repositories/{}/{}/commit/{}'.format(
            self.base_url, self.team,
            repo_name, commit_hash
        )
        req = requests.get(url, auth=self.auth)
        return req.json()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--branch", type=str, default="master")
    parser.add_argument("--pipeline", type=str, required=True)
    parser.add_argument("--pipe-vars", type=str)
    return parser.parse_args()


def main():
    bb = BitBucket(os.getenv('BB_CLIENT'), os.getenv('BB_TOKEN'), 'neurohive')
    args = parse_args()
    pipe_vars = None
    if args.pipe_vars:
        pipe_vars = json.loads(args.pipe_vars)
    bb.start_custom_pipeline(args.repo, args.branch, args.pipeline, pipe_vars)


def check_branch():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', type=str, required=True)
    parser.add_argument('--project-name', type=str, required=True)
    args = parser.parse_args()
    bb = BitBucket(os.environ['BB_CLIENT'], os.environ['BB_TOKEN'], 'neurohive')
    if bb.if_branch_in_prs(args.project_name, args.branch):
        print("found in pull requests")
        sys.exit()
    else:
        print("not in pull requests")
        sys.exit(1)


if __name__ == '__main__':
    pass
