import os
import sys
import logging
import argparse

from jira import JIRA

logger = logging.getLogger()

JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_TOKEN = os.getenv('JIRA_TOKEN')

if not JIRA_TOKEN or not JIRA_USERNAME:
    logging.error('Enter credentials JIRA_TOKEN|JIRA_USERNAME')
    sys.exit(1)


def add_comment(server, task_id, comment, comment_file):
    if comment_file:
        comment = comment_file.read()
    jira = JIRA(
        server=server,
        basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
    jira.add_comment(task_id, comment)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', required=True)
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--comment')
    parser.add_argument('--comment-file', type=argparse.FileType('r'))
    args = parser.parse_args()
    try:
        add_comment(args.server, args.task_id, args.comment, args.comment_file)
    except Exception as e:
        logger.error("Unable to comment jira task")
        logger.error(e)
