#!/usr/bin/env python3

# Standard libraries
from collections import OrderedDict
from os import environ
from os.path import expandvars
from pathlib import Path
from re import match

# Modules libraries
from dotenv import dotenv_values
from oyaml import safe_load as yaml_safe_load

# Components
from ..containers.images import Images
from ..features.menus import MenusFeature
from ..types.volumes import Volumes

# GitLab class
class GitLab:

    # Constants
    LOCAL_NODE = '.local'

    # Specifications
    JOB_STAGE_DEFAULT = 'test'
    STAGES_DEFAULT = {
        'build': 1,
        'test': 2,
        'deploy': 3,
    }

    # Environment
    ENV_JOB_NAME = 'CI_JOB_NAME'
    ENV_PROJECT_DIR = 'CI_PROJECT_DIR'

    # Members
    __options = None

    # Constructor
    def __init__(self, options):

        # Prepare options
        self.__options = options

    # Scripts
    @staticmethod
    def __scripts(items):

        # Variables
        scripts = []

        # Parse scripts data
        if isinstance(items, str):
            scripts = [items]
        elif isinstance(items, list):
            scripts = []
            for item in items:
                if isinstance(item, str):
                    scripts += [item]
                elif isinstance(item, list):
                    scripts += item[:]

        # Result
        return scripts

    # Globals
    def __globals(self, data, global_values, stages):

        # Iterate through nodes
        for node in data:

            # Filter image node
            if node == 'image':
                if not global_values['image']:
                    image_data = data[node]
                    if isinstance(image_data, dict):
                        global_values['image'] = expandvars(image_data['name'])
                        if 'entrypoint' in image_data and len(
                                image_data['entrypoint']) > 0:
                            global_values['entrypoint'] = image_data['entrypoint'][:]
                        else:
                            global_values['entrypoint'] = None
                    else:
                        global_values['image'] = expandvars(image_data)
                        global_values['entrypoint'] = None
                continue

            # Filter before_script node
            if node == 'before_script':
                global_values['before_script'] = self.__scripts(data[node])
                continue

            # Filter after_script node
            if node == 'after_script':
                global_values['after_script'] = self.__scripts(data[node])
                continue

            # Filter services node
            if node == 'services' and isinstance(data[node], list):
                global_values['services'] = []
                for item in data[node]:
                    if isinstance(item, dict):
                        global_values['services'] = [item.get('name', '')]
                    elif isinstance(item, str):
                        global_values['services'] += [item]
                continue

            # Filter stages node
            if node == 'stages':
                for i, stage in enumerate(data['stages']):
                    stages[stage] = i
                continue

            # Filter variables node
            if node == 'variables':
                for variable in data['variables']:
                    if variable not in global_values['variables']:
                        if data['variables'][variable] is None:
                            global_values['variables'][variable] = ''
                        else:
                            global_values['variables'][variable] = str(
                                data['variables'][variable])
                continue

    # Include
    def __include(self, data):

        # Parse nested include
        if 'include' in data and data['include']:
            data_new = dict()

            # Prepare includes nodes
            data_include_list = []
            if isinstance(data['include'], dict):
                data_include_list = [data['include']]
            elif isinstance(data['include'], list):
                data_include_list = data['include']
            elif isinstance(data['include'], str):
                data_include_list = [{'local': data['include']}]

            # Iterate through includes nodes
            for include_node in data_include_list:

                # Parse local nodes
                if 'local' in include_node:
                    file_path = include_node['local'].lstrip('/')
                    if (Path(self.__options.path) / file_path).is_file():
                        with open(Path(self.__options.path) / file_path,
                                  'r') as include_data:
                            include_additions = yaml_safe_load(include_data)
                            data_new.update(include_additions)

            # Agregate included data
            data_new.update(data)
            data = data_new
            data_new = None

        # Result
        return data

    # Local
    def __local(self, data, global_values):

        # Variables
        names_local = False

        # Filter local node
        if GitLab.LOCAL_NODE in data and data[GitLab.LOCAL_NODE]:
            local = data[GitLab.LOCAL_NODE]

            # Parse local after
            if 'after' in local:
                if self.__options.after:
                    self.__options.after = local['after']

            # Parse local all
            if 'all' in local:
                if not self.__options.all:
                    self.__options.all = local['all']

            # Parse local bash
            if 'bash' in local:
                if not self.__options.bash:
                    self.__options.bash = local['bash']

            # Parse local before
            if 'before' in local:
                if self.__options.before:
                    self.__options.before = local['before']

            # Parse local debug
            if 'debug' in local:
                if not self.__options.debug:
                    self.__options.debug = local['debug']

            # Parse local defaults
            if 'defaults' in local:
                if not self.__options.defaults:
                    self.__options.defaults = local['defaults']

            # Parse local engine
            if 'engine' in local:
                if self.__options.engine_default:
                    self.__options.engine = local['engine']
                    self.__options.engine_default = False

            # Parse local env
            if 'env' in local:
                for env in local['env']:
                    env_parsed = env.split('=', 1)

                    # Parse VARIABLE=value
                    if len(env_parsed) == 2:
                        variable = env_parsed[0]
                        value = env_parsed[1]
                        if variable not in global_values['variables']:
                            environ[variable] = value
                            global_values['variables'][variable] = value

                    # Parse ENVIRONMENT_FILE
                    elif (Path(self.__options.path) / env).is_file():
                        environment_file = Path(self.__options.path) / env
                        environment_file_values = dotenv_values(
                            dotenv_path=environment_file)
                        for variable in environment_file_values:

                            # Define default environment variable
                            if variable not in global_values['variables']:
                                global_values['variables'][
                                    variable] = environment_file_values[variable]

                    # Parse VARIABLE
                    else:
                        variable = env
                        if variable not in global_values['variables']:
                            if variable in environ:
                                global_values['variables'][variable] = environ[variable]
                            else:
                                global_values['variables'][variable] = ''

            # Parse local image
            if 'image' in local:
                if not self.__options.image:
                    self.__options.image = local['image']

            # Parse local manual
            if 'manual' in local:
                if not self.__options.manual:
                    self.__options.manual = local['manual']

            # Parse local names
            if 'names' in local:
                if not self.__options.names and not self.__options.pipeline:
                    names_local = True
                    self.__options.names = local['names']

            # Parse local network
            if 'network' in local:
                if not self.__options.network:
                    self.__options.network = local['network']

            # Parse local pipeline
            if 'pipeline' in local:
                if not self.__options.pipeline and (not self.__options.names
                                                    or names_local):
                    self.__options.pipeline = local['pipeline']

            # Parse local quiet
            if 'quiet' in local:
                if not self.__options.quiet:
                    self.__options.quiet = local['quiet']

            # Parse local real_paths
            if 'real_paths' in local:
                if not self.__options.real_paths:
                    self.__options.real_paths = local['real_paths']

            # Parse local sockets
            if 'sockets' in local:
                if not self.__options.sockets:
                    self.__options.sockets = local['sockets']

            # Parse local tags
            if 'tags' in local:
                if self.__options.tags_default:
                    self.__options.tags = local['tags'][:]
                    self.__options.tags_default = False

            # Parse local volumes
            if 'volumes' in local:
                if not self.__options.volume:
                    self.__options.volume = []
                for volume in local['volumes']:
                    self.__options.volume += [Volumes.LOCAL_FLAG + volume]

            # Parse local workdir
            if 'workdir' in local:
                if not self.__options.workdir:
                    self.__options.workdir = Volumes.LOCAL_FLAG + local['workdir']

            # Parse local configurations
            if 'configurations' in local:
                configured_variables = MenusFeature(options=self.__options).configure(
                    local['configurations'])
                global_values['variables'].update(configured_variables)

    # Parse
    def parse(self, data, environment):

        # Variables
        global_values = dict({
            'after_script': [],
            'before_script': [],
            'image': '',
            'entrypoint': None,
            'services': [],
            'variables': dict()
        })
        jobs = dict()
        stages = dict()

        # Parse nested include
        data = self.__include(data)

        # Prepare parameters variables
        if environment['parameters']:
            global_values['variables'].update(environment['parameters'])

        # Filter local node
        self.__local(data, global_values)

        # Prepare default variables
        if environment['default']:
            for variable in environment['default']:
                if variable not in global_values['variables']:
                    if variable in environ:
                        global_values['variables'][variable] = environ[variable]
                    else:
                        global_values['variables'][variable] = environment['default'][
                            variable]
                if variable not in environ:
                    environ[variable] = global_values['variables'][variable]

        # Prepare global image
        if self.__options.image:
            if isinstance(self.__options.image, dict):
                global_values['image'] = expandvars(self.__options.image['name'])
                if 'entrypoint' in self.__options.image and len(
                        self.__options.image['entrypoint']) > 0:
                    global_values['entrypoint'] = self.__options.image['entrypoint'][:]
                else:
                    global_values['entrypoint'] = None
            else:
                global_values['image'] = expandvars(self.__options.image)
                global_values['entrypoint'] = None

        # Global nodes
        self.__globals(data, global_values, stages)

        # Prepare environment
        _environ = dict(environ)
        environ.update(global_values['variables'])

        # Prepare defaults
        if not stages:
            stages = GitLab.STAGES_DEFAULT.copy()

        # Iterate through nodes
        for node in data:

            # Ignore global nodes
            if node in [
                    'after_script', 'before_script', 'image', 'include', 'services',
                    'stages', 'variables'
            ]:
                continue

            # Validate job node
            if 'script' not in data[node] and 'extends' not in data[node]:
                continue

            # Ignore template stage
            if node[0:1] == '.':
                continue

            # Register job
            jobs[node] = self.job(node, data, global_values)

            # Validate job script
            if not jobs[node]['options']['disabled'] and not jobs[node]['script']:
                raise ValueError('Missing "script" key for "%s / %s"' %
                                 (jobs[node]['stage'], jobs[node]['name']))

            # Append unknown stage if required
            if jobs[node]['options']['disabled'] and jobs[node][
                    'stage'] == GitLab.JOB_STAGE_DEFAULT and GitLab.JOB_STAGE_DEFAULT not in stages:
                stages[GitLab.JOB_STAGE_DEFAULT] = list(stages.values())[-1] + 1

            # Validate job stage
            if jobs[node]['stage'] not in stages:
                raise ValueError('Unknown stage "%s" for "%s"' %
                                 (jobs[node]['stage'], jobs[node]['name']))

        # Sort jobs based on stages
        jobs = OrderedDict(sorted(jobs.items(), key=lambda x: stages[x[1]['stage']]))

        # Restore environment
        environ.clear()
        environ.update(_environ)

        # Result
        return jobs

    # Job
    def job(self, job_name, data, global_values):

        # Variables
        job = dict()
        job_data = data[job_name]

        # Prepare stage
        job['name'] = job_name
        job['stage'] = None
        job['image'] = None
        job['entrypoint'] = None
        job['variables'] = None
        job['before_script'] = None
        job['script'] = None
        job['after_script'] = None
        job['retry'] = None
        job['when'] = None
        job['allow_failure'] = None
        job['services'] = None
        job['tags'] = None
        job['trigger'] = None
        job['options'] = dict()
        job['options']['disabled'] = None
        job['options']['host'] = False
        job['options']['quiet'] = False
        job['options']['silent'] = False
        job['options']['sockets'] = False
        job['options']['env_job_name'] = self.ENV_JOB_NAME
        job['options']['env_job_path'] = self.ENV_PROJECT_DIR

        # Extract job extends
        if 'extends' in job_data and job_data['extends']:
            if isinstance(job_data['extends'], list):
                job_extends = job_data['extends']
            else:
                job_extends = [job_data['extends']]

            # Iterate through extended jobs
            for job_extend in reversed(job_extends):

                # Parse extended job
                if job_extend not in data:
                    job['options']['disabled'] = '%s unknown' % (job_extend)
                    if job['stage'] is None:
                        job['stage'] = GitLab.JOB_STAGE_DEFAULT
                    break
                job_extended = self.job(job_extend, data, None)

                # Extract extended job
                if job['stage'] is None:
                    job['stage'] = job_extended['stage']
                if job['image'] is None:
                    job['image'] = job_extended['image']
                if job['entrypoint'] is None:
                    job['entrypoint'] = job_extended['entrypoint']
                if job['variables'] is None:
                    job['variables'] = job_extended['variables']
                elif job_extended['variables']:
                    for variable in job_extended['variables']:
                        job['variables'][variable] = job_extended['variables'][variable]
                if job['before_script'] is None:
                    job['before_script'] = job_extended['before_script']
                if job['script'] is None:
                    job['script'] = job_extended['script']
                if job['after_script'] is None:
                    job['after_script'] = job_extended['after_script']
                if job['retry'] is None:
                    job['retry'] = job_extended['retry']
                if job['when'] is None:
                    job['when'] = job_extended['when']
                if job['allow_failure'] is None:
                    job['allow_failure'] = job_extended['allow_failure']
                if job['services'] is None:
                    job['services'] = job_extended['services']
                if job['tags'] is None:
                    job['tags'] = job_extended['tags']
                if job['trigger'] is None:
                    job['trigger'] = job_extended['trigger']

        # Apply global values
        if global_values:
            if job['image'] is None:
                job['image'] = global_values['image']
            if job['entrypoint'] is None:
                job['entrypoint'] = global_values['entrypoint'][:] if global_values[
                    'entrypoint'] else None
            if job['variables'] is None:
                job['variables'] = dict(global_values['variables'])
            else:
                for variable in global_values['variables']:
                    if variable not in job['variables']:
                        job['variables'][variable] = global_values['variables'][variable]
            if job['before_script'] is None:
                job['before_script'] = global_values['before_script'][:]
            if job['script'] is None:
                job['script'] = []
            if job['after_script'] is None:
                job['after_script'] = global_values['after_script'][:]
            if job['retry'] is None:
                job['retry'] = 0
            if job['services'] is None:
                job['services'] = global_values['services'][:]
            if job['when'] is None:
                job['when'] = 'on_success'
            if job['allow_failure'] is None:
                job['allow_failure'] = False

        # Apply template values
        else:
            if job['variables'] is None:
                job['variables'] = {}

        # Extract job stage
        if 'stage' in job_data and job_data['stage']:
            job['stage'] = job_data['stage']
        elif job['stage'] is None:
            job['stage'] = GitLab.JOB_STAGE_DEFAULT

        # Extract job image
        if 'image' in job_data and job_data['image']:
            image_data = job_data['image']
            if isinstance(image_data, dict):
                job['image'] = expandvars(image_data['name'])
                if 'entrypoint' in image_data and len(image_data['entrypoint']) > 0:
                    job['entrypoint'] = image_data['entrypoint'][:]
                else:
                    job['entrypoint'] = None
            else:
                job['image'] = expandvars(image_data)
                job['entrypoint'] = None

        # Extract job variables
        if 'variables' in job_data and job_data['variables']:
            for variable in job_data['variables']:
                if job_data['variables'][variable] is None:
                    job['variables'][variable] = ''
                else:
                    job['variables'][variable] = str(job_data['variables'][variable])

        # Extract job before_script
        if 'before_script' in job_data:
            job['before_script'] = self.__scripts(job_data['before_script'])

        # Extract job script
        if 'script' in job_data:
            job['script'] = self.__scripts(job_data['script'])

        # Extract job after_script
        if 'after_script' in job_data:
            job['after_script'] = self.__scripts(job_data['after_script'])

        # Extract job retry
        if 'retry' in job_data:
            retry_data = job_data['retry']
            if isinstance(retry_data, dict):
                job['retry'] = int(retry_data['max'])
            else:
                job['retry'] = int(retry_data)

        # Extract job when
        if 'when' in job_data and job_data['when'] in [
                'on_success', 'on_failure', 'always', 'manual'
        ]:
            job['when'] = job_data['when']

        # Extract job allow_failure
        if 'allow_failure' in job_data and job_data['allow_failure'] in [True, False]:
            job['allow_failure'] = job_data['allow_failure']

        # Extract job services
        if 'services' in job_data and isinstance(job_data['services'], list):
            job['services'] = []
            for item in job_data['services']:
                if isinstance(item, dict):
                    job['services'] += [item.get('name', '')]
                elif isinstance(item, str):
                    job['services'] += [item]

        # Extract job tags
        if 'tags' in job_data and job_data['tags']:
            job['tags'] = job_data['tags'][:]

        # Extract job trigger
        if 'trigger' in job_data and job_data['trigger']:
            job['options']['disabled'] = 'trigger only'
            if isinstance(job_data['trigger'], (dict, str)):
                job['trigger'] = job_data['trigger']

        # Finalize global values
        if global_values:

            # Configure job tags
            if job['tags'] and (set(job['tags']) & set(self.__options.tags)):
                job['when'] = 'manual'

        # Detect host jobs
        if job['image']:
            job['options']['host'] = Images.host(job['image'])
            job['options']['quiet'] = Images.quiet(job['image'])
            job['options']['silent'] = Images.silent(job['image'])

        # Detect sockets services
        if job['services']:
            for service in job['services']:
                if match(Images.DOCKER_DIND_REGEX, service):
                    job['options']['sockets'] = True

        # Result
        return job
