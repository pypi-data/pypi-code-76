import dpath.util


INDENT_LENGTH = 4

class ConfigReader:
    def __init__(self, configuration_filepath):
        self._configuration_filepath = configuration_filepath
        self._configuration_file = None
        self._config = {}
    
    def read(self):
        with open(self._configuration_filepath, 'r') as fc:
            self._configuration_file = fc.read()
        
        self._set_config()
        
        return self._configuration_file

    def _set_config(self):
        parent_config_path = ''
        config = []

        for config_line in self._configuration_file.split('\n'):
            config_level = int((len(config_line) - len(config_line.lstrip())) / INDENT_LENGTH)
            config_line = config_line.lstrip()

            if not config_line:
                continue

            key, value = (config_line.split()[0], config_line.split()[1:])
            if key in ['config', 'edit']:
                path = key + ' ' + ' '.join(value)
                parent_config_path += path + '/'
                config.append({'set': {}, 'unset': {}})

            if key in ['set', 'unset']:
                if len(value) == 1:
                    value.append('')
                config[config_level - 1][key][value[0]] = ' '.join(value[1:])

            if key in ['end', 'next']:
                try:
                    current = dpath.util.get(self._config, parent_config_path[:-1])
                    if not config[-1] == {'set': {}, 'unset': {}}:
                        config[-1].update(current)
                        dpath.util.set(self._config, parent_config_path[:-1], config[-1])
                except:
                    dpath.util.new(self._config, parent_config_path[:-1], config[-1])
                config.pop()
                parent_config_path = '/'.join(parent_config_path[:-1].split('/')[:-1]) + '/'

    def get_config(self):
        return self._config
