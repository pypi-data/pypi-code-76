"""
    utils functions
"""
import yaml


def init_config(file_name: str = './example.yaml'):
    """
        Util method that creates an example config at the given file_name
        args:
            file_name (str): full path to config YAML file
    """
    config = {
        'queryConfig': [{
            'endpoint': 'stat',
            'parameters': [
                {'stats': 'list',
                 'list': 'alert subscribers'}]}]}

    # write to file
    with open(file_name, 'w') as file_:
        yaml.dump(config, file_)
