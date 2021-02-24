import os
import argparse
import logging
import sys

from neurohive.integration.bitbucket import BitBucket, BitBucketException


def bb_is_branch_exists():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", "-p", type=str, required=True)
    parser.add_argument("--branch", "-b", type=str, required=True)
    args = parser.parse_args()

    bb = BitBucket(os.getenv('BB_CLIENT'), os.getenv('BB_TOKEN'), 'neurohive')
    branches = bb.find_branches(args.project, args.branch)
    logging.basicConfig(level=logging.INFO)
    logging.info(branches)
    if branches:
        sys.exit(0)
    else:
        sys.exit(1)


def bb_create_branch():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", "-p", type=str, required=True)
    parser.add_argument("--branch", "-b", type=str, required=True)
    parser.add_argument("--target-hash", type=str, required=False, default="master")
    args = parser.parse_args()
    bb = BitBucket(os.getenv('BB_CLIENT'), os.getenv('BB_TOKEN'), 'neurohive')
    new_branch = bb.create_branch(args.project, args.branch, target_hash=args.target_hash)
    print(new_branch)


def bb_create_pr():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", "-r", type=str, required=True)
    parser.add_argument("--title", "-t", type=str, required=True)
    parser.add_argument("--src-branch", "-s", type=str, required=True)
    parser.add_argument("--dest-branch", "-d", type=str, required=False, default="master")
    args = parser.parse_args()
    bb = BitBucket(os.getenv('BB_CLIENT'), os.getenv('BB_TOKEN'), 'neurohive')
    status = bb.create_pr(args.repo, args.title, args.src_branch, args.dest_branch)
    print(status)
