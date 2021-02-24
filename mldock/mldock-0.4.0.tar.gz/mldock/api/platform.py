import os
import json
import logging
from pathlib import Path
from future.moves import subprocess

from mldock.config.config_manager import \
    ResourceConfigManager, PackageConfigManager, \
        HyperparameterConfigManager, InputDataConfigManager
from mldock.api.local import \
    _copy_boilerplate_to_dst, _rename_file

logger=logging.getLogger('mldock')

def _write_json(obj, path):  # type: (object, str) -> None
    """Write a serializeable object as a JSON file."""
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)
        f.write('\n')

def generic_init(dir, helper_library_path, mldock_config, testing_framework, service, container_only, template_dir):

    logger.info("Initializing Assets - Generic Container")
    src_directory = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src")
    )
    service_directory = os.path.join(
        dir,
        'service'
    )

    logger.info("getting template")

    if template_dir is None:
        template_dir = os.path.join(
            helper_library_path,
            "templates",
            mldock_config['platform']
        )
        logger.debug("--- no template dir provided, using = (Default) {}".format(mldock_config['platform']))

    logger.debug("Template directory = {}".format(template_dir))


    mldock_module_path = os.path.join(
        src_directory,
        'container'
    )

    test_path = os.path.join(mldock_module_path, 'local_test', 'test_dir')

    logger.info("Setting up workspace")   
    logger.debug("Adding container")
    _copy_boilerplate_to_dst(
        os.path.join(template_dir,'src/container'),
        mldock_module_path,
        remove_first=True
    )
    if container_only == False:
        logger.debug("Adding src scripts")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'src/'), src_directory)

    if testing_framework == 'pytest':
        logger.info("Adding pytest container tests")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'tests/'), 'tests/')
        logger.debug("renaming test file")

        _rename_file(
            base_path='tests/container_health',
            current_filename='_template_test_container.py',
            new_filename='test_{ASSET_DIR}.py'.format(ASSET_DIR=dir)
        )
    if service is not None:
        logger.info("Adding {} service".format(service))
        _copy_boilerplate_to_dst(os.path.join(template_dir,'service',service), service_directory)

def _make_sagemaker_input_data_configs(data_channels: list):
    """restructures a list of data names as sagemaker input data configs"""
    return {name: {} for name in data_channels}

def _extract_data_channels_from_mldock(mldock_data: list):

    data_channels = [
        data_config['channel'] for data_config in mldock_data
    ]

    return _make_sagemaker_input_data_configs(data_channels=data_channels)

def sagemaker_init(dir, helper_library_path, mldock_config, no_prompt, testing_framework, service, container_only, template_dir):

    logger.info("Initializing Assets - Sagemaker Container")
    src_directory = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src")
    )

    service_directory = os.path.join(
        dir,
        'service'
    )

    logger.info("getting template")

    if template_dir is None:
        template_dir = os.path.join(
            helper_library_path,
            "templates",
            mldock_config['platform']
        )
        logger.debug("--- no template dir provided, using = (Default) {}".format(mldock_config['platform']))

    logger.debug("Template directory = {}".format(template_dir))

    mldock_module_path = os.path.join(
        src_directory,
        'container'
    )

    test_path = os.path.join(mldock_module_path, 'local_test', 'test_dir')

    logger.info("Setting up workspace")   
    logger.debug("Adding container")
    _copy_boilerplate_to_dst(
        os.path.join(template_dir,'src/container'),
        mldock_module_path,
        remove_first=True
    )
    if container_only == False:
        logger.debug("Adding src scripts")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'src'), src_directory)

    if testing_framework == 'pytest':
        logger.info("Adding pytest container tests")
        _copy_boilerplate_to_dst(os.path.join(template_dir,'tests'), 'tests')
        logger.debug("renaming test file")

        _rename_file(
            base_path='tests/container_health',
            current_filename='_template_test_container.py',
            new_filename='test_{ASSET_DIR}.py'.format(ASSET_DIR=dir)
        )

    if service is not None:
        logger.info("Adding {} service".format(service))
        _copy_boilerplate_to_dst(os.path.join(template_dir, 'service', service), service_directory)

    logger.info("Adding dummy sagemaker goodies")
    _write_json({}, Path(dir,'config/hyperparameters.json'))

    # get list of dataset names
    mldock_data = mldock_config.get("data", None)
    input_config_config = _extract_data_channels_from_mldock(mldock_data)
    _write_json(input_config_config, Path(dir,'config/inputdataconfig.json'))
    _write_json({"current_host": "dummy_host", "hosts": ["dummy_host", "second_dummy_host"]}, Path(dir,'config/resourceconfig.json'))
