# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess
import traceback
import uuid
from jinja2 import Template
from datetime import datetime
from trainingopz.builders_and_generators.packager.packager import Packager
from trainingopz.exceptions.packager_error import PackagerError
from trainingopz.project_config import ProjectConfig
from trainingopz.utilities.parser.config_parser import ConfigParser
from trainingopz.utilities.parser.cmd_config_parser import CmdConfigParser


class DockerPackager(Packager):

    # ---------------------------------------- #
    # ------------- Construction ------------- #
    # ---------------------------------------- #

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__workflows_path: str = os.path.join(kwargs.get('project_path'), 'workflows')

        self._pipelines: list = list()
        self._pacified_tasks: list = list()

        self.__docker_config = ConfigParser().parse().docker_config()

        __cmd_config_obj = CmdConfigParser()
        __cmd_config_obj.parse()
        self.__cmd_config = __cmd_config_obj.configuration()

        self.__dockerfile_templates = self._populate_dockerfile_templates()
        self.__cached_docker_images = {}

    @classmethod
    def _populate_dockerfile_templates(cls) -> dict:
        dockerfile_templates = {}
        template_root = os.path.join(ProjectConfig.package_root(), 'templates/docker_templates')
        for file in os.listdir(template_root):
            if os.path.isfile(os.path.join(template_root, file)) and file.lower().endswith('_dockerfile'):
                dockerfile_templates[file.strip('_dockerfile')] = os.path.join(template_root, file)

        return dockerfile_templates

    # ---------------------------------------- #
    # -------------- Public API -------------- #
    # ---------------------------------------- #

    def build_part(self, **kwargs):

        try:
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.build_part for {kwargs};")
            if 'pipelines' not in kwargs.keys():
                error_message = f"In {__name__}.build_part 'pipelines' was not found in build_part. " \
                                f"The parameters passed were: {' - '.join(kwargs.keys()) }."

                self._logger.exception(error_message)
                raise ValueError(error_message)

            self._build(pipelines=kwargs.get("pipelines"))
            self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}.build_part;")
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    # ----------------------------------------- #
    # ------------ Execution Logic ------------ #
    # ----------------------------------------- #

    def _build(self, pipelines: list) -> None:
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}._build for {pipelines};")
        self._workflows = []
        for pipeline in pipelines:
            updated_pipes: list = list()
            while len(pipeline['workflow']) > 0:
                for pipe in pipeline['workflow']:
                    _res = self.__build_docker_image(pipe=pipe)

                    if _res['successful']:
                        # Update dependencies pacified
                        self._pacified_tasks.append(pipe['stage_name'])
                        # Make a copy of the new pipes
                        updated_pipes.append(pipe)
                        # Remove old pipe
                        pipeline['workflow'].remove(pipe)

            self._build_flows.append(
                {
                    'name': pipeline['name'],
                    'workflow': updated_pipes
                }
            )
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}._build;")

    def __build_docker_image(self, pipe: dict) -> dict:
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__build_docker_image for {pipe};")
        # TODO Below are unnecessary renamings - the only thing that should remain is repo_tagged_docker_image_name.
        pipe.update(
            {
                'repo_tagged_docker_image_name': None,
            }
        )

        if pipe.get("cmd_type"):
            pipe.update(self.__cmd_config[pipe["cmd_type"]])

        if pipe.get('type') in self.__cached_docker_images.keys():
            self._logger.info(f"Docker image has been built in a previous step - bypassing build process.")
            pipe['repo_tagged_docker_image_name'] = self.__cached_docker_images[pipe.get('type')]
            return dict(
                successful=True,
                pipe=pipe
            )

        # TODO - This is only for 'pythonic' packages. Need to abstract the build process into another class that allows for specialization on this.
        build_config = dict(
            docker_file=os.path.abspath(os.path.join(self.__root_path, 'Dockerfile_' + uuid.uuid4().hex)),
            requirements_txt='requirements.txt',
            image_name=pipe.get('type').lower().replace(' ', '_'),
        )

        # --------------------------- #
        # --- Build Docker Images --- #
        # --------------------------- #

        if pipe.get('dependencies') and not self.__are_dependencies_pacified(pipe.get('dependencies')):
            return dict(successful=False)

        # ------------------------- #
        # --- Create Dockerfile --- #
        # ------------------------- #

        try:
            # Create Parameters for Dockerfile Jinja Template

            with open(self.__dockerfile_templates[pipe['type']], 'r') as fh:
                docker_file_text = Template(fh.read(), autoescape=True).render(
                    requirements=build_config['requirements_txt'],
                    executable_app=pipe['fit']
                )

            # Save Dockerfile to disk
            with open(build_config['docker_file'], 'w') as fh:
                fh.write(docker_file_text)
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')
        self._logger.info('Docker image created.')

        # ---------------------------------------- #
        # --- Build + Tag + Publish Dockerfile --- #
        # ---------------------------------------- #
        cur_dir = os.getcwd()
        os.chdir(self.__root_path)
        try:
            root = pipe['fit'].split(os.sep)[0]
            _ = subprocess.run(['zip', '-r', 'files_to_add.zip', root], check=True)

            build_results = subprocess.run(['docker', 'build', '-t', build_config['image_name'], '-f', build_config['docker_file'], '.'], check=True)

            self._logger.info(f'Build Results: {build_results}')

            os.remove('files_to_add.zip')

            image_name = build_config['image_name']
            repo_tagged_docker_image_name = self.__docker_config['docker_registry'] + '/' + image_name

            tag_name = str(uuid.uuid1())
            repo_tagged_docker_image_name = repo_tagged_docker_image_name + ":" + tag_name

            #  TODO: make more pythonic
            job_id = os.environ.get('JOB_ID')
            repo_tagged_docker_image_name = repo_tagged_docker_image_name + "-" + str(job_id)

            tag_results = subprocess.run(['docker', 'tag', image_name, repo_tagged_docker_image_name], check=True)
            self._logger.info(f'Tag Results: {tag_results}')

            push_results = subprocess.run(['docker', 'push', repo_tagged_docker_image_name], check=True)
            self._logger.info(f'Push Results: {push_results}')

            pipe['repo_tagged_docker_image_name'] = repo_tagged_docker_image_name
            self.__cached_docker_images[pipe['type']] = repo_tagged_docker_image_name
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')
        finally:
            os.chdir(cur_dir)
        self._logger.info('Docker image built.')

        # ------------------------- #
        # --- Delete Dockerfile --- #
        # ------------------------- #
        try:
            os.remove(build_config['docker_file'])
            if not os.path.exists(build_config['docker_file']):
                return dict(
                    successful=True
                )
            else:
                self.__handle_exception(f"Removal Dockerfile {build_config['docker_file']} has failed.")
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__build_docker_image;")

    def __handle_exception(self, message: str) -> None:
        message = f'In {__name__}: {message}'
        self._logger.exception(message)
        raise(PackagerError(message))

    def __are_dependencies_pacified(self, dependencies: list) -> bool:
        return len([1 for dependency in dependencies if dependency in self._pacified_tasks]) == len(dependencies)
