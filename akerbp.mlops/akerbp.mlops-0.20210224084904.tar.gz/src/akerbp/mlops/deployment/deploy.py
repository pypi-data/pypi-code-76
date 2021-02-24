"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions. 
Model registry uses CDF Files.
""" 
import os
import traceback
import shutil

import akerbp.mlops.model_manager as mm
from akerbp.mlops.deployment import helpers, platforms
from akerbp.mlops.core import logger, config
logging=logger.get_logger(name='mlops_deployment')
env = config.envs.env
service_name = config.envs.service_name

platform_methods = platforms.get_methods()

def deploy_model(model_settings, platform_methods=platform_methods):

    c = model_settings
    logging.debug(" ")
    logging.info(f"Deploy model {c.model_name}")

    deployment_folder =f'mlops_{c.model_name}'
    function_name=f"{c.model_name}-{service_name}-{env}"

    if service_name == 'prediction':
        c.model_id = mm.set_up_model_artifact(
            c.artifact_folder, 
            c.model_name
        )

    m = "Create deployment folder and move required files/folders"
    logging.info(m)
    os.mkdir(deployment_folder)
    
    helpers.copy_to_deployment_folder(c.files, deployment_folder)

    logging.debug(f"cd {deployment_folder}")
    os.chdir(deployment_folder)
    
    helpers.set_up_requirements(c)

    config.store_service_settings(c)

    # * Dependencies: (user settings <- model test). Either run before
    #   going to the dep. folder or copy project config to dep. folder. 
    # * It is important to run tests after setting up the artifact
    #   folder in case it's used to test prediction service.
    # * Tests need the model requirements installed!
    logging.info(f"Run model and service tests")
    input, check = helpers.get_model_test_data(c.test_import_path)
    if c.test_file:
        helpers.run_tests(c.test_file)
        from akerbp.mlops.services.test_service import test_service
        test_service(input, check)
    else:
        logging.warning("Model test file is missing! Didn't run tests")


    logging.info(f"Deploy {function_name} to {c.platform}")
    deploy_function, test_function = platform_methods[c.platform]
    deploy_function(function_name, info=c.info[service_name])
    
    if c.test_import_path:
        logging.info("Make a test call")
        test_function(function_name, input)
    else:
        logging.warning("No test file was set up. End-to-end test skipped!")


def deploy(project_settings):
    failed_models = {}
    base_path = os.getcwd()
        
    for c in project_settings:
        model_name = c.model_name
        deployment_folder =f'mlops_{model_name}'
        try:
            deploy_model(c)
        except Exception:
            trace = traceback.format_exc()
            error_message = f"Model failed to deploy!\n{trace}"
            logging.error(error_message)
            
            failed_models[model_name] = error_message
        finally:
            logging.debug(f"cd ..")
            os.chdir(base_path)
            logging.debug(f"Delete deployment folder")
            if os.path.isdir(deployment_folder):
                shutil.rmtree(deployment_folder)

    if failed_models:
        for model_name, error_message in failed_models.items():
            logging.debug(" ")
            logging.info(f"Model {model_name} failed: {error_message}")
        raise Exception("At least one model failed.")


if __name__ == '__main__':
    mm.setup()
    s = config.read_project_settings()
    deploy(s)