# config.py
import os
import traceback
from typing import List, Optional
from pydantic.dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
import yaml

from akerbp.mlops.core import helpers 
from akerbp.mlops.core import logger

logging=logger.get_logger(name='mlops_core')


def validate_categorical(setting, name, allowed):
    if setting not in allowed:
        m = (f"{name}: allowed values are {allowed}, got '{setting}'")
        raise ValueError(m)


@dataclass
class EnvVar():
    env: str
    service_name: Optional[str] = None
    google_project_id: Optional[str] = None
    platform: Optional[str] = None
    local_deployment: bool = False

    def __post_init__(self):        
        validate_categorical(self.env, "Environment", ["dev", "test", "prod"])
        validate_categorical(self.platform, "Platform", ["cdf", "gc", None])
        if self.env != 'dev':
            validate_categorical(self.service_name, "Service  name", 
                ["training", "prediction"])


# Read environmental variables
def read_env_vars():
    """
    Read environmental variables and initialize EnvVar object with those that
    were set (i.e. ignored those with None value)
    """
    envs=dict(
        env=os.getenv('ENV'), 
        service_name=os.getenv('SERVICE_NAME'), 
        local_deployment=os.getenv('LOCAL_DEPLOYMENT'),
        google_project_id=os.getenv('GOOGLE_PROJECT_ID'),
        deployment_platform=os.getenv('DEPLOYMENT_PLATFORM'),
    )
    envs = {k:v for k,v in envs.items() if v}
    return EnvVar(**envs)

envs = read_env_vars()
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


def generate_default_project_settings(
    yaml_file='mlops_settings.yaml', 
    n_models=2
):
    if os.path.isfile(yaml_file):
        raise Exception(f"Settings file {yaml_file} exists already.")
    
    default_config = [ 
"""
model_name: my_model
model_file: model_code/my_model.py
req_file: model_code/requirements.model
test_file: model_code/test_model.py
artifact_folder: artifact_folder
platform: cdf
info:
    prediction: 
        description: Description prediction service for my_model
        owner: datascientist@akerbp.com
    training:
        << : *desc
        description: Description training service for my_model
"""
    ]
    default_config *= n_models
    default_config = "---".join(default_config)
    with open(yaml_file, 'w') as f:
        f.write(default_config)


def validate_model_reqs(req_file):
    if not os.path.isfile(req_file):
        raise ValueError(f"File {req_file} does not exist")
    # Model reqs is renamed to requirements.txt during deployment
    elif 'requirements.model' in req_file:
        with open(req_file, 'r') as f: 
            req_file_string = f.read()
            if 'akerbp.mlops' not in req_file_string:
                m = 'Model requirements should include akerbp.mlops package'
                raise Exception(m)
            if 'MLOPS_VERSION' not in req_file_string:
                m = 'akerbp.mlops version should be "MLOPS_VERSION"'
                raise Exception(m)


@dataclass
class ServiceSettings():
    model_name: str # Remember to modify generate_default_project_settings()
    model_file: Path # if fields are modified
    req_file: Path
    test_file: Path
    artifact_folder: Path
    info: dict
    platform: str = 'cdf'
    model_id: Optional[str] = None

    def __post_init__(self):
        # Validation
        if not os.path.isfile(self.model_file):
            raise ValueError(f"File {self.model_file} does not exist")

        validate_model_reqs(self.req_file)

        validate_categorical(self.platform, "Deployment platform", 
            ["cdf", "gc", "local"])

        if self.platform == 'gc' and not envs.google_project_id:
            raise Exception("Platform 'gc' requires GOOGLE_PROJECT_ID env var")

        if self.model_id and envs.service_name == 'training':
            raise ValueError("Unexpected model_id setting (training service)")

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
                "install_req_file.sh":("akerbp.mlops.gc", "install_req_file.sh")
            }
            self.files = {**self.files, **files_gc}


def store_service_settings(c, yaml_file='mlops_service_settings.yaml'):
    logging.info("Write service settings file")

    def factory(data):
        """
        Take a list of tuples as input. Returns a suitable dictionary.
        Transforms Path objects to strings (linux style path).
        """
        path2str = lambda x: x if not isinstance(x,Path) else x.as_posix()
        d = {k:path2str(v) for k,v in data}
        return d
    
    service_settings=asdict(c, dict_factory=factory)
    with open(yaml_file, 'w') as f:
        yaml.dump(service_settings,f)


@dataclass
class ProjectSettings():
    project_settings: List[ServiceSettings]


def read_project_settings(yaml_file='mlops_settings.yaml'):
    logging.info(f"Read project settings")
    with open(yaml_file, 'r') as f:
        settings = yaml.safe_load_all(f.read())
    model_settings = [ServiceSettings(**s) for s in settings]
    project_settings = ProjectSettings(project_settings=model_settings)
    logging.debug(f"{project_settings=}")        
    return project_settings.project_settings


def read_service_settings(yaml_file='mlops_service_settings.yaml'):
    logging.info(f"Read service settings")
    with open(yaml_file, 'r') as f:
        settings = yaml.safe_load(f.read())
    service_settings = ServiceSettings(**settings)
    logging.debug(f"{service_settings=}")
    return service_settings


def validate_user_settings(yaml_file='mlops_settings.yaml'):
    try:
        read_project_settings(yaml_file)
        logging.info("Settings file is ok :)")
    except Exception:
        trace = traceback.format_exc()
        error_message = f"Settings file is not ok! Fix this:\n{trace}"
        logging.error(error_message)



