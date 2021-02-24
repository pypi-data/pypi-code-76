import os
import argparse
import re
from datetime import datetime
import logging

from neurohive.integration.bitbucket import BitBucket
from neurohive.integration.unitycloud import UnityCloud
from neurohive.integration.appcenter import AppCenter
from neurohive.deploy.ecs import AwsEcsDeploy
from ..deploy.compose_conv import convert_compose_to_vars
from ..deploy.kube import prep_ustate_kube_versions
from ..deploy.unity import update_unity_ios_creds
from ..buildinfo.info import GitChanges
from ..deploy.string import slugify


def get_jira_name_from_branch(branch_name):
    match = re.search(r'(feature|bugfix)?(?P<name>\w+-\d+)', branch_name)
    if match:
        return match.groupdict()['name']


def create_uc_builds_from_branches(uc_client, branches, src_build_target):
    now = datetime.now().strftime('%Y-%m-%d-%H%M')
    to_build = []
    for branch in branches:
        jira_name = get_jira_name_from_branch(branch)
        name = f'AutoPR-{now}--{branch}'
        if jira_name:
            name = f'AutoPR-{now}--{jira_name}'
        to_build.append({
            "branch": branch,
            "target_name": name
        })
    targets_data = []
    for build in to_build:
        logging.info(f'Create build: {build}')
        targets_data.append(uc_client.clone_build_target(src_build_target, build['target_name'], build['branch']))
    return targets_data


def create_and_build_from_prs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-project", type=str, required=True)
    parser.add_argument("--unity-project", type=str, required=True)
    parser.add_argument("--src-build-target-name", type=str, required=True)
    args = parser.parse_args()

    bb = BitBucket(os.getenv('BB_CLIENT'), os.getenv('BB_TOKEN'), 'neurohive')
    uc = UnityCloud(os.getenv('UNITY_ORG_ID', 'unity_oekd8fheerjomw'), project_name=args.unity_project)

    # удаляю прошлые сборки )
    logging.basicConfig(level=logging.INFO)
    uc.remove_target_with_prefix('AutoPR')
    # получаю список веток с открытими prs
    opened_prs = bb._get_opened_pr(args.git_project)
    branches = [branch['source']['branch']['name'] for branch in opened_prs]
    build_targets = create_uc_builds_from_branches(uc, branches, args.src_build_target_name)
    # запускаю
    for build_target in build_targets:
        uc._create_build(build_target['buildtargetid'])


def cleanup_old_appcenter_build():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-name", type=str, required=True)
    parser.add_argument("--owner", type=str, required=True)
    parser.add_argument("--leave-num", type=int, default=10)
    args = parser.parse_args()
    ac = AppCenter(args.owner)
    ac.cleanup_old_builds(args.app_name, args.leave_num)


def deploy_ecs_task():
    parser = argparse.ArgumentParser()
    parser.add_argument("--def-settings-dir", type=str, required=True)
    parser.add_argument("--codedeploy-settings", type=str, required=True)
    args = parser.parse_args()
    ecs = AwsEcsDeploy(args.def_settings_dir, args.codedeploy_settings)
    ecs.create_deploy()


def prepare_compose_vars():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compose-file', type=str, required=True)
    parser.add_argument('--vars-file', type=str, required=True)
    args = parser.parse_args()
    convert_compose_to_vars(args.compose_file, args.vars_file)


def prepare_ustate_kube_values():
    parser = argparse.ArgumentParser()
    parser.add_argument("--values-file", type=str, required=True)
    parser.add_argument("--namespace", type=str, required=True)
    args = parser.parse_args()
    prep_ustate_kube_versions(args.namespace, args.values_file)


def update_unity_creds():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True, help="Unity CB Project Name")
    parser.add_argument("--target", type=str, required=True, help="Unity CB Target Name")
    parser.add_argument("--bundle", type=str, required=True, help="iOS bundle id")
    parser.add_argument("--prov-type", type=str, required=True, help="iOS provision type")
    args = parser.parse_args()
    update_unity_ios_creds(args.project, args.target, args.bundle, args.prov_type)


def get_ac_dl_link():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", type=str, required=True)
    parser.add_argument("--app", type=str, required=True)
    parser.add_argument("--build-ver", type=str, required=True)
    args = parser.parse_args()
    ac = AppCenter(args.owner)
    print(ac.get_download_link(args.app, args.build_ver))


def get_git_changelog():
    logging.basicConfig(level=logging.ERROR)
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=str, required=True, help="Dynamo table name")
    parser.add_argument("--base-branch", type=str, required=True, help="base branch")
    args = parser.parse_args()
    gc = GitChanges(os.getcwd(), args.base_branch, args.table)
    print(gc.show_changes())


def slugify_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("--string", type=str, required=True)
    args = parser.parse_args()
    print(slugify(args.string))
