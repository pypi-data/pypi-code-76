import json
import os
import logging

logger = logging.getLogger()


def read_service_configuration(configuration_file, section=0):
    """

    :param configuration_file:
    :param section:
    :return:
    """
    try:

        if section:
            service_configuration = json.load(open(configuration_file)).get(section)
        else:
            service_configuration = json.load(open(configuration_file))
        return service_configuration
    except Exception as error:
        logger.error("EXCEPTION opening service configuration:", error)
        return 0


def check_configuration_directory():
    """

    :return:
    """
    service_configuration_directory = os.environ.get('service_configuration_directory', 'configuration')
    if os.path.isdir(service_configuration_directory):
        return os.getcwd() + service_configuration_directory
    else:
        return False


def write_data_to_json_file(data_to_persit, filename):
    """
    this method stores data_to_persit to the given filename

    :param data_to_persit:
    :param filename:
    :return:
    """
    try:
        file_to_open = filename
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(file_to_open))
        with open(file_to_open, 'w') as outfile:
            json.dump(data_to_persit, outfile)
            logger.info(
                'Service Configuration stored to %s\n' % filename)
            return 1
    except Exception as error:
        logger.error(
            'Exception %s occurred writing data to a file %s \n' % (error, data_to_persit))
        return 0
