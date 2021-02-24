from subprocess import run

import boto3


class GitChanges:
    def __init__(self, repo_dir, base_branch, table_name):
        self.repo_dir = repo_dir
        self.base_branch = base_branch
        self.client = boto3.client('dynamodb')
        self.table_name = table_name

    def show_changes(self):
        curr_branch = self._get_current_branch()
        curr_hash = self._get_current_hash()
        last_hash = self._get_hash_from_dynamo(curr_branch)
        if not last_hash:
            changelog = self._get_diff_between(self.base_branch, curr_branch)
            self._put_hash_to_dynamo(curr_branch, curr_hash)
            return changelog
        else:
            changelog = self._get_diff_between(last_hash, curr_hash)
            self._put_hash_to_dynamo(curr_branch, curr_hash)
            if not changelog:
                return "Ничего нового."
            else:
                return changelog

    def _get_diff_between(self, last, cur):
        cmd = ['git', 'log', '--oneline', '--no-color', f'{last}..{cur}']
        proc = run(cmd, capture_output=True, timeout=2)
        return proc.stdout.decode('utf-8')

    def _get_current_hash(self):
        cmd = ['git', "log", "--pretty=%H", "-1"]
        proc = run(cmd, capture_output=True, timeout=2)
        return proc.stdout.decode('utf-8').split('\n')[0]

    def _get_current_branch(self):
        cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        proc = run(cmd, capture_output=True, timeout=2)
        return proc.stdout.decode('utf-8').split('\n')[0]

    def _get_hash_from_dynamo(self, branch):
        resp = self.client.get_item(
            TableName=self.table_name,
            Key={
                'branch': {
                    'S': branch
                }
            }
        )
        if 'Item' in resp:
            return resp['Item']['hash']['S']

    def _put_hash_to_dynamo(self, branch, hash):
        resp = self.client.put_item(  # noqa: F841
            TableName=self.table_name,
            Item={
                'branch': {
                    'S': branch,
                },
                'hash': {
                    'S': hash
                }
            }
        )
