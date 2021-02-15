#setup.py
import os
from akerbp.mlops import __version__ as version
from akerbp.mlops.core import logger 
from akerbp.mlops.deployment.helpers import to_folder, replace_string_file

logging=logger.get_logger(name='MLOps')


def setup_pipeline(folder_path='.'):
    """
    Set up pipeline file in the given folder
    """
    # Extract package resource
    pipeline_file = 'bitbucket-pipelines.yml'
    pipeline = ('akerbp.mlops.deployment', pipeline_file)
    to_folder(pipeline, folder_path)
    pipeline_path = os.path.join(folder_path, pipeline_file) 
    # Set package version in the pipeline
    replace_string_file('MLOPS_VERSION', version, pipeline_path)

