# config.py
import os
from typing import List, Optional
from pydantic.dataclasses import dataclass
from dataclasses import asdict
import yaml

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
envs=EnvVar(
    env=os.getenv('ENV'), 
    service_name=os.getenv('SERVICE_NAME'), 
    local_deployment=os.getenv('LOCAL_DEPLOYMENT'),
    google_project_id=os.getenv('GOOGLE_PROJECT_ID'),
    deployment_platform=os.getenv('DEPLOYMENT_PLATFORM'),
)
envs_dir=asdict(envs)
logging.debug(f"{envs_dir=}")

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
class ServiceSettings():
    model_name: str
    model_file: str
    req_file: str
    test_file: str
    artifact_folder: str
    platform: str
    info: dict
    model_id: Optional[str] = None

    def __post_init__(self):
        # Validation
        if not os.path.isfile(self.model_file):
            raise ValueError(f"File {self.model_file} does not exist")

        if not os.path.isfile(self.req_file):
            raise ValueError(f"File {self.req_file} does not exist")

        
        if self.platform not in ["cdf", "gc", "local"]:
            m = f"Deployment platform should be either 'cdf', 'gc' or 'local'"
            raise ValueError(m)

    def __post_init_post_parse__(self):
        # Derived fields
        if envs.env == 'dev' and not envs.local_deployment:
            self.platform = 'local'
        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.test_file)

        self.files = {
            "model code": helpers.get_top_folder(self.model_file), 
            "handler": (f"akerbp.mlops.cdf","handler.py"),
            "artifact folder": self.artifact_folder
        }
        if self.platform == "gc":
            files_gc = {
                "Dockerfile": ("akerbp.mlops.gc", "Dockerfile"),
                "requirements.app": ("akerbp.mlops.gc", "requirements.app"),
                "install_req_file.sh": ("akerbp.mlops.gc", "install_req_file.sh")
            }
            self.files = {**self.files, **files_gc}


def store_service_settings(c):
    logging.info("Write service settings file")
    service_settings=asdict(c)
    with open('mlops_service_settings.yaml', 'w') as f:
        yaml.dump(service_settings,f)


@dataclass
class ProjectSettings():
    project_settings: List[ServiceSettings]


def read_config():
    if os.path.isfile('mlops_settings.yaml'):
        logging.info(f"Read project settings")
        with open('mlops_settings.yaml', 'r') as f:
            settings = yaml.safe_load_all(f.read())
        model_settings = [ServiceSettings(**s) for s in settings]
        project_settings = ProjectSettings(project_settings=model_settings)
        logging.debug(f"{project_settings=}")        
        return project_settings
    elif os.path.isfile('mlops_service_settings.yaml'):
        logging.info(f"Read service configuration")
        with open('mlops_service_settings.yaml', 'r') as f:
            settings = yaml.safe_load(f.read())
        service_settings = ServiceSettings(**settings)
        logging.debug(f"{service_settings=}")
        return service_settings
    else:
        raise Exception("Didn't find a suitable settings file")
