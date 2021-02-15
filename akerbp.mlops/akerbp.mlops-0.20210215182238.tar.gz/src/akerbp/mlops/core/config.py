# config.py
import os
from typing import List, Optional
from importlib import import_module
from pydantic.dataclasses import dataclass
from dataclasses import asdict

from akerbp.mlops.core import helpers 
from akerbp.mlops.core import logger

logging=logger.get_logger(name='MLOps')


@dataclass
class EnvVar():
    env: str
    service_name: str
    local_deployment: Optional[str]
    google_project_id: Optional[str]

    def __post_init__(self):
        envs = ["dev", "test", "prod"]
        if self.env not in envs:
            m = (f"Environment: allowed values are {envs}"
                 f", got '{self.env}'")
            raise ValueError(m)

        service_names = ["training", "prediction"]
        if self.service_name not in service_names:
            m = (f"Service name: allowed values are {service_names}"
                 f", got '{self.env}'")
            raise ValueError(m)

        local_deployments = ["True", None]
        if self.local_deployment not in local_deployments:
            m = (f"Local deployment: allowed values are {local_deployments}"
                 f", got '{self.env}'")
            raise ValueError(m)

# Read environmental variables
_getenv=EnvVar(
    env=os.getenv('ENV'), 
    service_name=os.getenv('SERVICE_NAME'), 
    local_deployment=os.getenv('LOCAL_DEPLOYMENT'),
    google_project_id=os.getenv('GOOGLE_PROJECT_ID')
)
getenv=asdict(_getenv)
logging.debug(getenv)

@dataclass
class CdfKeys():
    data: Optional[str]
    files: Optional[str]
    functions: Optional[str]

_api_keys = CdfKeys(
   data = os.environ['COGNITE_API_KEY_DATA'],
   files = os.environ['COGNITE_API_KEY_FILES'],
   functions = os.environ['COGNITE_API_KEY_FUNCTIONS']
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
    model_artifact_folder: str
    info: dict
    model_test_file: str
    deployment_platform: str

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
        from akerbp.mlops.gc.helpers import deploy_function as gc_deploy
        from akerbp.mlops.gc.helpers import test_function as gc_test
        from akerbp.mlops.cdf.helpers import deploy_function as cdf_deploy
        from akerbp.mlops.cdf.helpers import test_function as cdf_test
        from akerbp.mlops.cdf.helpers import set_up_cdf_client
        
        # Derived fields
        if _getenv.env == 'dev' and not _getenv.local_deployment:
            self.deployment_platform = 'local'
        
        if self.deployment_platform == 'cdf':
            set_up_cdf_client(context='deploy')
            self.deploy_function, self.test_function = cdf_deploy, cdf_test
        elif self.deployment_platform == 'gc': 
            self.deploy_function, self.test_function = gc_deploy, gc_test
        elif self.deployment_platform == 'local': 
            self.deploy_function=self.test_function=lambda *args,**kargs: None

        self.model_code_folder = helpers.get_top_folder(self.model_file)
        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.model_test_file)

        self.files = {
            "model code": self.model_code_folder, 
            "handler": (f"akerbp.mlops.cdf","handler.py"),
            "project config": 'mlops_settings.py',
            "artifact folder": self.model_artifact_folder
        }
        if self.deployment_platform == "gc":
            files_gc = {
                "Dockerfile": ("akerbp.mlops.gc", "Dockerfile"),
                "requirements.app": ("akerbp.mlops.gc", "requirements.app"),
                "install_req_file.sh": ("akerbp.mlops.gc", "install_req_file.sh")
            }
            self.files = {**self.files, **files_gc}

    def post_model_reqs(self):
        service_test = import_module(self.test_import_path).ServiceTest()
        self.input = getattr(service_test, f"{_getenv.service_name}_input")
        self.check = getattr(service_test, f"{_getenv.service_name}_check")


@dataclass
class ProjectConfig():
    model_settings: List[ModelConfig]


def read_config():
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

project_settings = read_config()


def get_model_config(model_name):
    for setting in project_settings.model_settings:
        if model_name == setting.model_name:
            return setting
    raise ValueError(f"Didn't find settings for {model_name=}")

