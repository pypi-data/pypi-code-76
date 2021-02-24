import yaml

def load_config(file_stream):
    return yaml.load(file_stream, Loader=yaml.SafeLoader)
