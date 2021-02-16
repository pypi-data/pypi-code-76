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
locals().update(config.getenv)




platform_methods = platforms.get_methods()


def deploy_model(model_settings, platform_methods=platform_methods):

    c = model_settings
    logging.debug(" ")
    logging.info(f"Deploy model {c.model_name}")

    deployment_folder =f'mlops_{c.model_name}'
    function_name=f"{c.model_name}-{service_name}-{env}"

    if service_name == 'prediction':
        model_id = mm.set_up_model_artifact(
            c.model_artifact_folder, 
            c.model_name
        )
    else:
        model_id = None

    m = "Create deployment folder and move required files/folders"
    logging.info(m)
    os.mkdir(deployment_folder)
    
    helpers.copy_to_deployment_folder(c.files, deployment_folder)

    logging.debug(f"cd {deployment_folder}")
    os.chdir(deployment_folder)

    logging.info("Write service settings file")
    mlops_settings=dict(
        model_name=c.model_name,
        model_artifact_folder=c.model_artifact_folder,
        model_import_path=c.model_import_path,
        model_code_folder=c.model_code_folder,
        model_id=model_id,
        test_import_path=c.test_import_path
    )
    # File name can't be mlops_settings.py, or there will be an
    # importing error when the service test is run (user settings <-
    # model test <- service test)
    with open('service_settings.py', 'w') as config_file:
        config_file.write(f'{mlops_settings=}')
    
    helpers.set_up_requirements(c.model_req_file)

    # * Dependencies: (user settings <- model test). Either run before
    #   going to the dep. folder or copy project config to dep. folder. 
    # * It is important to run tests after setting up the artifact
    #   folder in case it's used to test prediction service.
    # * Tests need the model requirements installed!
    logging.info(f"Run model and service tests")
    input, check = helpers.get_model_test_data(c.test_import_path)
    if c.model_test_file:
        helpers.run_tests(c.model_test_file)
        from akerbp.mlops.services.test_service import test_service
        test_service(input, check)
    else:
        logging.warning("Model test file is missing! Didn't run tests")


    logging.info(f"Deploy {function_name} to {c.deployment_platform}")
    deploy_function, test_function = platform_methods[c.deployment_platform]
    deploy_function(function_name, info=c.info[service_name])
    
    if c.test_import_path:
        logging.info("Make a test call")
        test_function(function_name, input)
    else:
        logging.warning("No test file was set up. End-to-end test skipped!")


def deploy():
    failed_models = {}
    base_path = os.getcwd()
    
    
    for model_settings in config.project_settings.model_settings:
        model_name = model_settings.model_name
        deployment_folder =f'mlops_{model_name}'
        try:
            deploy_model(model_settings)
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
    deploy()