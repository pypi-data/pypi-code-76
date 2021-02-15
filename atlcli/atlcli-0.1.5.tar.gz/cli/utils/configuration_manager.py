from os.path import expanduser
import yaml
import base64

class ConfigurationManager:
    DEFAULT_CONFIG_FILE_PATH = expanduser("~")+"/.gdlf_config.yml"

    def __init__(self):
        pass

    def load_config(self):
        try:
            with open(self.DEFAULT_CONFIG_FILE_PATH) as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
            return data
        except IOError:            
            return None        
        

    def create_config(self, data):
        credentials = "{username}:{password}".format(username = data["credentials"]["username"],
            password = data["credentials"]["password"])
        encodedBytes = base64.b64encode(credentials.encode("utf-8"))
        data["credentials"]["base64"] = str(encodedBytes, "utf-8")
        
        with open(self.DEFAULT_CONFIG_FILE_PATH, 'w') as file:
            yaml.dump(data, file)
