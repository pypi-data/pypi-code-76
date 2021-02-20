import mxdevtool as mx
import mxdevtool.utils as utils
import os, json


class DefaultRepository:
    def __init__(self):
        self.scen_log = dict()

    def logging_scen(self, scenario):
        hashCode = utils.get_hashCode(scenario)
        jsonStr = json.dumps(scenario.toDict())

        self.scen_log[hashCode] = jsonStr


class FolderRepository:
    def __init__(self, config):
        if isinstance(config, str):
            self.config = {'location': config}
        else:
            self.config = config

        self.paths = dict()
        self.xenarix_manager = None
        self.shock_manager = None

        self.initialize()

    def initialize(self):
        from mxdevtool.xenarix import XenarixFileManager
        from mxdevtool.shock import ShockFileManager

        repo_path = self.config['location']

        # xenarix 
        xen_path = os.path.join(repo_path, 'xenarix')
        if not os.path.exists(xen_path):
            os.makedirs(xen_path)
        xfm_config = { 'location': xen_path }
        self.xenarix_manager = XenarixFileManager(xfm_config)
        self.paths['xenarix'] = xen_path

        # shock
        shock_path = os.path.join(repo_path, 'shock')
        if not os.path.exists(shock_path):
            os.makedirs(shock_path)
        sfm_config = { 'location': shock_path }
        self.shock_manager = ShockFileManager(sfm_config)
        self.paths['shock'] = shock_path

        # logging
        log_path = os.path.join(repo_path, 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.paths['log'] = log_path

    def logging_scen(self, scen):
        hashCode = utils.get_hashCode(scen)
        jsonStr = json.dumps(scen.toDict())
        filename = os.path.join(self.paths['log'], hashCode)
        f = open(filename, "w")
        f.write(jsonStr)
        f.close()

    def get_log_scen(self, hashCode):
        if not hashCode in histories:
            raise Exception('hashcode does not exist - {0}'.format(hashCode))
