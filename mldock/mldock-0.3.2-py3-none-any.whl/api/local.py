import os
import sys
import json
import logging
from pathlib import Path
import docker
import traceback
import logging
import signal

from distutils.dir_util import copy_tree, remove_tree
from distutils.dir_util import mkpath
from distutils.file_util import write_file
from future.moves import subprocess

logger=logging.getLogger('mldock')


def train_model(working_dir, docker_tag, image_name, entrypoint, cmd, env=None):
    """
    Trains ML model(s) locally
    :param working_dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    process_env = None
    if env is not None:
        process_env = os.environ.copy()
        process_env.update(env)

    client = docker.from_env()

    try:
        container = client.containers.run(
            image="{image}:{tag}".format(image=image_name, tag=docker_tag),
            entrypoint=entrypoint,
            command=cmd,
            environment=process_env,
            remove=True,
            tty=True,
            volumes={
                '{test_path}/config'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/config', 'mode': 'rw'},
                '{test_path}/data'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/data', 'mode': 'rw'},
                '{test_path}/model'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/model', 'mode': 'rw'},
                '{test_path}/output'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/output', 'mode': 'rw'}
            },
            auto_remove=True,
            detach=True,
            stream=True
        )
        logs = container.logs(follow=True).decode('utf-8')

        logger.info(logs)
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
        container.kill()
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def deploy_model(working_dir, docker_tag, image_name, entrypoint, cmd, port=8080, env={}):
    """
    Deploys ML models(s) locally
    :param working_dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """

    process_env = os.environ.copy()
    if isinstance(env, dict) & len(env) > 0:
        process_env.update(env)
    client = docker.from_env()

    try:
        container = client.containers.run(
            image="{image}:{tag}".format(image=image_name, tag=docker_tag),
            entrypoint=entrypoint,
            command=cmd,
            environment=process_env,
            ports={8080: port},
            remove=True,
            tty=True,
            volumes={
                '{test_path}/config'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/config', 'mode': 'rw'},
                '{test_path}/data'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/data', 'mode': 'rw'},
                '{test_path}/model'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/model', 'mode': 'rw'},
                '{test_path}/output'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/output', 'mode': 'rw'}
            },
            auto_remove=True,
            detach=True,
            stream=True
        )
        logs = container.logs(follow=True).decode('utf-8')

        logger.info(logs)
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
        container.kill()
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.info(exception)
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def pretty_build_logs(line: dict):

    if line is None:
        return None
    error = line.get('error', None)
    errorDetail = line.get('errorDetail', None)
    if error is not None:
        logger.error('{}\n{}'.format(error, errorDetail))
    
    stream = line.get('stream','')

    if ('Step' in stream) & (':' in stream):
        logger.info(stream)
    else:
        logger.debug(stream)

def docker_build(
    image_name: str,
    dockerfile_path: str,
    module_path: str,
    target_dir_name: str,
    requirements_file_path: str,
    no_cache: bool,
    client = None
):
    """Runs the build executable from script path, passing a set of arguments in a command line subprocess.

    Args:
        script_path (str): relative path to script when run on root
        base_path (str):
        image_name (str):
        dockerfile_path (str):
        module_path (str):
        target_dir_name (str):
        requirements_file_path (str):
    """

    # if client is None:
        # client = docker.from_env()
    client = docker.APIClient(base_url=os.environ.get('DOCKER_HOST','tcp://127.0.0.1:1234'))

    try:
        short_log = []

        logs = client.build(
            tag=image_name,
            path='.',
            dockerfile=os.path.join(dockerfile_path, 'Dockerfile'),
            buildargs={
                'module_path': module_path,
                'target_dir_name': target_dir_name,
                'requirements_file_path': requirements_file_path
            },
            quiet=False,
            nocache=no_cache,
            rm=True,
            decode=True
        )

        for line in logs:
            pretty_build_logs(line=line)
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.info(exception)
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def _write_file(filepath, parents=True):
    """write a file"""
    if parents == True:
        mkpath(str(Path(filepath).parents[0].absolute()))
    write_file(str(Path(filepath).absolute()), '')

def _rename_file(base_path, current_filename, new_filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, current_filename).rename(Path(base_path, new_filename))

def _create_empty_file(base_path, filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, filename).touch(exist_ok=True)

def _copy_boilerplate_to_dst(src: str, dst: str, remove_first=False):
    """[summary]

    Args:
        src (str): [description]
        dst (str): [description]
    """
    source_path = str(Path(src).absolute())
    destination_path = str(Path(dst).absolute())
    if remove_first == True:
        try:
            logger.debug("removing first")
            remove_tree(destination_path)
        except FileNotFoundError as exception:
            logger.debug("No file found. Assuming already deleted.")
    response = copy_tree(source_path, destination_path)
