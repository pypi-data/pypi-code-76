import os
import subprocess
from subprocess import CalledProcessError
import logging
import json
from copy import deepcopy

import boto3

from neurohive.deploy.templates import APPSPEC

logger = logging.getLogger()


class AwsEcsDeployException(Exception):
    pass


class AwsEcsDeploy:
    def __init__(self, def_dir, cd_settings):
        self.def_dir = def_dir
        self.cd_settings = cd_settings
        self._check_reqs()

    def create_deploy(self):
        self.prep_task_from_settings_dir()
        appspec_string = self._prep_appspec()
        with open(self.cd_settings, 'rt') as fp:
            deploy = json.load(fp)
        deploy['revision']['appSpecContent']['content'] = appspec_string
        client = boto3.client('codedeploy')

        try:
            resp = client.create_deployment(**deploy)
            if 'deploymentId' not in resp:
                raise AwsEcsDeployException("Deployment failed")
        except Exception as e:
            logger.error(e)
            raise

    def _prep_appspec(self):
        task_def = self._get_terraform_output()['task_def']['value']
        appspec = deepcopy(APPSPEC)
        tg_props = appspec['Resources'][0]['TargetService']['Properties']
        tg_props['TaskDefinition'] = task_def['arn']
        tg_props['LoadBalancerInfo']['ContainerName'] = task_def['lb_continer_name']
        tg_props['LoadBalancerInfo']['ContainerPort'] = task_def['lb_container_port']
        return json.dumps(appspec)

    def prep_task_from_settings_dir(self):
        # NOTE Seems unused, to removal
        # settings_path = os.path.abspath(self.def_dir)
        self._init_terraform()
        self._apply_terraform()

    def _get_terraform_output(self):
        cmd = ['terraform', 'output', '-no-color', '-json']
        try:
            output = json.loads(subprocess.run(cmd, cwd=self.def_dir, check=True, capture_output=True).stdout)
            return output
        except CalledProcessError as e:
            logger.error('terraform output failed')
            raise AwsEcsDeployException(e)

    def _init_terraform(self):
        try:
            cmd = ['terraform', 'init']
            subprocess.run(cmd, cwd=self.def_dir, check=True)
        except CalledProcessError as e:
            logger.error('terraform init failed')
            raise AwsEcsDeployException(e)

    def _apply_terraform(self):
        cmd = ['terraform', 'apply', '-auto-approve', '-no-color']
        try:
            subprocess.run(cmd, cwd=self.def_dir, check=True)
        except CalledProcessError as e:
            logger.error("failed to apply terraform changes")
            raise AwsEcsDeployException(e)

    def _check_reqs(self):
        try:
            os.environ['AWS_SECRET_ACCESS_KEY']
            os.environ['AWS_ACCESS_KEY_ID']
        except KeyError as e:
            logger.error("AWS Credentials required")
            raise AwsEcsDeployException(e)

        try:
            subprocess.run(['terraform', '-v'], check=True)
        except CalledProcessError as e:
            logger.error("terraform executin checks failed")
            raise AwsEcsDeployException(e)
        except FileNotFoundError:
            logger.error("terraform required")
            raise AwsEcsDeployException()

        if not os.path.isdir(self.def_dir):
            raise AwsEcsDeployException("Specify terraform task setup dir")
        if not os.path.isfile(self.cd_settings):
            raise AwsEcsDeployException("Specify codedeploy settings")
