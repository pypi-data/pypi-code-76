#setup.py
import os
from akerbp.mlops import __version__ as version
from akerbp.mlops.core import logger 
from akerbp.mlops.deployment.helpers import to_folder, replace_string_file
from  akerbp.mlops.core.config import generate_default_project_settings

logging=logger.get_logger(name='mlops_deployment')


def setup_pipeline(folder_path='.', overwrite=False):
    """
    Set up pipeline file in the given folder
    """
    pipeline_file = 'bitbucket-pipelines.yml'
    pipeline_path = os.path.join(folder_path, pipeline_file)
    if not overwrite and os.path.isfile(pipeline_path):
        m = f"File {pipeline_file} exists already in folder '{folder_path}'"
        raise Exception(m)
    # Extract package resource
    pipeline = ('akerbp.mlops.deployment', pipeline_file)
    to_folder(pipeline, folder_path)
    # Set package version in the pipeline
    replace_string_file('MLOPS_VERSION', version, pipeline_path)



if __name__ == '__main__':
    logging.info("Create pipeline file")
    setup_pipeline() 
    logging.info("Create settings file template")
    generate_default_project_settings()
    logging.info("Done!")

