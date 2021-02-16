import logging
import os
import shutil
import subprocess
import time

from madeira_utils import loggers, utils


class DockerDev(object):

    def __init__(self, api_image_tag="latest", ui_image_tag="latest", debug=False):
        self._logger = loggers.get_logger(level=logging.DEBUG if debug else logging.INFO)

        self.base_dir = os.getcwd()
        self._logger.debug('Using base dir: %s', self.base_dir)

        app_config = utils.load_yaml('config.yaml')
        self.app_type = app_config['app_type']
        self.app_config = app_config['test']

        self.app_name = self.app_config['name']
        self.app_name_lower = self.app_config['name'].lower()

        self.api_config_secret_name = f"{self.app_name}_config"
        self.api_image_name = f"{self.app_name_lower}_api"
        self.api_image_tag = api_image_tag
        self.api_image_local_path = f"{self.api_image_name}:{self.api_image_tag}"

        self.ui_image_name = f"{self.app_name_lower}_ui"
        self.ui_image_tag = ui_image_tag
        self.ui_image_local_path = f"{self.ui_image_name}:{self.ui_image_tag}"

    def _build_image(self, name, file):
        self._logger.info(f"Building container image: {name} using file: {file}")
        return self.run_command(f"docker build -t {name} . --file ./docker/{file}".split(" "))

    def _prune_images(self):
        self._logger.info("Pruning any dangling docker images")
        return self.run_command("docker image prune -f".split(" "))

    def build_api(self):
        if self.app_type != 'cloudfront_app':
            self._logger.warning(
                'Building API container image not supported for app type: %s', self.app_type)
            return

        self._build_image(self.api_image_name, "Dockerfile_api")
        self._prune_images()

    def build_ui(self):
        self._build_image(self.ui_image_name, "Dockerfile_ui")
        self._prune_images()

    def run_api(self, mock_data=False, madeira_dev=False, shell=False):
        if self.app_type != 'cloudfront_app':
            self._logger.warning(
                'Running the API container not supported for app type: %s', self.app_type)
            return

        args = [
            "docker",
            "run",
            "--interactive",
            "--tty",
            "--rm"
        ]

        if mock_data:
            self._logger.info("Using mock data mode (no AWS credentials mapped)")
            args.extend([
                "--env", "MOCK_DATA=true",
                "--volume", f"{self.base_dir}/mock_data:/root/mock_data"
            ])
        else:
            args.extend([
                "--env", f"API_CONFIG_SECRET_NAME={self.api_config_secret_name}",
                "--volume", f"{os.path.expanduser('~/.aws/config:/root/.aws/config')}",
                "--volume", f"{os.path.expanduser('~/.aws/credentials:/root/.aws/credentials')}"
            ])
        if madeira_dev:
            self._logger.info("Using local copies of madeira and madeira-utils in container venv")
            container_py_lib_dir = "/root/.venv/lib/python3.8/site-packages"
            madeira_dir = os.path.abspath('../madeira/madeira')
            madeira_utils_dir = os.path.abspath('../madeira-utils/madeira_utils')

            args.extend([
                "--volume", f"{madeira_dir}:{container_py_lib_dir}/madeira",
                "--volume", f"{madeira_utils_dir}:{container_py_lib_dir}/madeira_utils"
            ])

        args.extend([
            "--volume", f"{self.base_dir}/api.py:/root/api.py",
            "--volume", f"{self.base_dir}/config.yaml:/root/config.yaml",
            "--volume", f"{self.base_dir}/gunicorn.py:/root/gunicorn.py",
            "--volume", f"{self.base_dir}/functions:/root/functions",
            "--volume", f"{self.base_dir}/layers:/root/layers",
            "-p", "0.0.0.0:8080:8080",
            "--name", self.api_image_name,
            "--hostname", self.api_image_name,
            "--network", "bridge"
        ])

        args.append(f"{self.api_image_local_path}")

        if shell:
            args.append("bash")
        else:
            args.extend("pipenv run gunicorn --config gunicorn.py api:api".split(' '))

        while True:
            self._logger.info("Starting API container")
            self.run_command(args)
            time.sleep(2)

    def run_dev(self, mock_data=False, madeira_dev=False, shell=False):

        xfce4_terminal = '/usr/bin/xfce4-terminal'

        if not os.path.exists(xfce4_terminal):
            self._logger.error("%s cannot be found", xfce4_terminal)
            return False

        pipenv = shutil.which('pipenv')
        api_command = f'{pipenv} run madeira-run-api'

        if mock_data:
            api_command += ' --mock-data'
        if madeira_dev:
            api_command += ' --madeira-dev'
        if shell:
            api_command += ' --shell'

        command = [
            xfce4_terminal,
            '--title', self.ui_image_name, '--command', f'{pipenv} run madeira-run-ui',
            '--tab', '--title', self.api_image_name, '--command', api_command
        ]

        for container in (self.api_image_name, self.ui_image_name):
            container_is_running = bool(self.run_command(
                f'docker ps -q -f name={container}'.split(' '), capture_output=True).stdout.decode('utf-8').strip())
            self._logger.debug("container: %s is running: %s", container, container_is_running)
            if container_is_running:
                self.run_command(f'docker stop {container}'.split(' '))

        self._logger.info("Starting terminal for %s dev", self.app_name)
        self.run_command(command)

    def run_ui(self):
        return self.run_command([
            "docker",
            "run",
            "--interactive",
            "--tty",
            "--rm",
            "--volume", f"{self.base_dir}/assets:/usr/share/nginx/html",
            "-p", "0.0.0.0:8083:80",
            "--name", self.ui_image_name,
            "--hostname", self.ui_image_name,
            "--network", "bridge",
            self.ui_image_local_path
        ])

    @staticmethod
    def run_command(args, **kwargs):
        return subprocess.run(args, **kwargs)
