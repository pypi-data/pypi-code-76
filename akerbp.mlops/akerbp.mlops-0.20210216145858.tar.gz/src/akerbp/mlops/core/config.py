# config.py
import os
from typing import List, Optional
from pydantic.dataclasses import dataclass
from dataclasses import asdict

from akerbp.mlops.core import helpers 
from akerbp.mlops.core import logger

logging=logger.get_logger(name='mlops_core')


@dataclass
class EnvVar():
    env: str
    service_name: Optional[str]
    local_deployment: Optional[str]
    google_project_id: Optional[str]
    deployment_platform: Optional[str]

    def __post_init__(self):
        envs = ["dev", "test", "prod"]
        if self.env not in envs:
            m = (f"Environment: allowed values are {envs}"
                 f", got '{self.env}'")
            raise ValueError(m)

        service_names = ["training", "prediction"]
        if self.env != 'dev' and self.service_name not in service_names:
            m = (f"Service name: allowed values are {service_names}"
                 f", got '{self.service_name}'")
            raise ValueError(m)

        local_deployments = ["True", None]
        if self.local_deployment not in local_deployments:
            m = (f"Local deployment: allowed values are {local_deployments}"
                 f", got '{self.local_deployment}'")
            raise ValueError(m)

        deployment_platforms = ["cdf", "gc", None]
        if self.deployment_platform not in deployment_platforms:
            m = (f"Local deployment: allowed values are {deployment_platforms}"
                 f", got '{self.deployment_platforms}'")
            raise ValueError(m)

# Read environmental variables
_getenv=EnvVar(
    env=os.getenv('ENV'), 
    service_name=os.getenv('SERVICE_NAME'), 
    local_deployment=os.getenv('LOCAL_DEPLOYMENT'),
    google_project_id=os.getenv('GOOGLE_PROJECT_ID'),
    deployment_platform=os.getenv('DEPLOYMENT_PLATFORM'),
)
getenv=asdict(_getenv)
logging.debug(f"{getenv=}")

@dataclass
class CdfKeys():
    data: Optional[str]
    files: Optional[str]
    functions: Optional[str]

_api_keys = CdfKeys(
   data = os.getenv('COGNITE_API_KEY_DATA'),
   files = os.getenv('COGNITE_API_KEY_FILES'),
   functions = os.getenv('COGNITE_API_KEY_FUNCTIONS')
)
api_keys = asdict(_api_keys)

def update_cdf_keys(new_keys):
    global api_keys
    api_keys=asdict(CdfKeys(**new_keys))


@dataclass
class ModelConfig():
    model_name: str
    model_file: str
    model_req_file: str
    model_test_file: str
    model_artifact_folder: str
    deployment_platform: str
    info: dict
    model_id: Optional[str] = None

    def __post_init__(self):
        # Validation
        if not os.path.isfile(self.model_file):
            raise ValueError(f"File {self.model_file} does not exist")

        if not os.path.isfile(self.model_req_file):
            raise ValueError(f"File {self.model_req_file} does not exist")

        
        if self.deployment_platform not in ["cdf", "gc", "local"]:
            m = f"Deployment platform should be either 'cdf', 'gc' or 'local'"
            raise ValueError(m)

    def __post_init_post_parse__(self):
        # Derived fields
        if _getenv.env == 'dev' and not _getenv.local_deployment:
            self.deployment_platform = 'local'
        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.model_test_file)

        self.files = {
            "model code": helpers.get_top_folder(self.model_file), 
            "handler": (f"akerbp.mlops.cdf","handler.py"),
            #"project config": 'mlops_settings.py',
            "artifact folder": self.model_artifact_folder
        }
        if self.deployment_platform == "gc":
            files_gc = {
                "Dockerfile": ("akerbp.mlops.gc", "Dockerfile"),
                "requirements.app": ("akerbp.mlops.gc", "requirements.app"),
                "install_req_file.sh": ("akerbp.mlops.gc", "install_req_file.sh")
            }
            self.files = {**self.files, **files_gc}


def store_model_config(c):
    logging.info("Write service settings file")
    model_settings=asdict(c)
    with open('mlops_model_settings.py', 'w') as config_file:
        config_file.write(f'{model_settings=}')


@dataclass
class ProjectConfig():
    model_settings: List[ModelConfig]


def read_config():
    if os.path.isfile('mlops_settings.py'):
        logging.info(f"Read project configuration")
        from mlops_settings import model_names, model_files, model_req_files
        from mlops_settings import model_artifact_folders, infos, model_test_files
        from mlops_settings import model_platforms
        settings = [dict(
            model_name=model_names[x],
            model_file=model_files[x],
            model_req_file=model_req_files[x],
            model_artifact_folder=model_artifact_folders[x],
            info=infos[x],
            model_test_file=model_test_files[x],
            deployment_platform=model_platforms[x]
        ) for x in range(len(model_names))]

        model_settings = [ModelConfig(**s) for s in settings]
        project_settings = ProjectConfig(model_settings=model_settings)
        logging.debug(f"{project_settings=}")
        
        return project_settings
    elif os.path.isfile('mlops_model_settings.py'):
        logging.info(f"Read service configuration")
        from mlops_model_settings import model_settings
        model_settings = ModelConfig(**model_settings)
        logging.debug(f"{model_settings=}")
        return model_settings
    else:
        raise Exception("Didn't find suitable settings file")




def get_model_config(model_name):
    for setting in project_settings.model_settings:
        if model_name == setting.model_name:
            return setting
    raise ValueError(f"Didn't find settings for {model_name=}")

