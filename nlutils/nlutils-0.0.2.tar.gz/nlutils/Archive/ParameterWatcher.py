import json

from hashlib import md5
from functools import singledispatch
from datetime import datetime
from ..Utils.Log import Logger
from ..CommonDefine import ParameterType, DEV_MODE, DevelopMode, ParameterHandlerOperation



PARAMETER_OPERATION_DISPATCHER_THEME = {
    ParameterType.MODEL: None,
    ParameterType.DATA: None,
    ParameterType.TRANINING: None,
    ParameterType.MISCELLANEOUS: None,
    'Initialized': False
}

VALID_OPERATION_TYPE = ('INSERT', 'DELETE', 'UPDATE', 'SELECT')
NECESSARY_KEYS = {'parameter_type', 'operation_type'}

PARAMETER_OPERATION_DISPATCHER_OP = {
    ParameterHandlerOperation.INSERT: None,
    ParameterHandlerOperation.DELETE: None,
    ParameterHandlerOperation.UPDATE: None,
    ParameterHandlerOperation.SELECT: None,
    'Initialized': False
}

def get_md5_hash(obj):
    md5_obj = md5()
    md5_obj.update(obj.encode('utf8'))
    return md5_obj.hexdigest()
class ParameterWatcher(object):

    def __init__(self):
        self.model_parameters = dict()
        self.training_parameters = dict()
        self.miscellaneous_parameters = dict()
        self.data_parameters = dict()
        self.models = dict()
        self.results = dict()
        self.id = get_md5_hash(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def insert_parameter(self, dic, pkg):
        Logger.get_logger().info("Inserting parameter package.")
        for key in pkg['insert_keys']:
            if key not in NECESSARY_KEYS:
                dic[key] = pkg[key]

    def delete_parameter(self, dic, pkg):
        Logger.get_logger().info("Deleting parameter package.")
        for key in pkg['delete_keys']:
            if key not in NECESSARY_KEYS:
                dic.pop(key)

    def update_parameter(self, dic, pkg):
        Logger.get_logger().info("Updating parameter package.")
        for key in pkg['update_keys']:
            if key not in NECESSARY_KEYS:
                dic[key] = pkg[key]
        

    def select_parameter(self, dic, pkg):
        Logger.get_logger().info("Selecting parameter package.")
        select_values = []
        for key in pkg['select_keys']:
            if key not in dic:
                select_values.append({key: dic[key]})
        return select_values

    def pkg_validation(self, pkg):
        for key in NECESSARY_KEYS:
            if key not in pkg.keys():
                return False
            if pkg is None:
                return False
        return True

    def main_operation_handler(self, dic, pkg):
        if PARAMETER_OPERATION_DISPATCHER_OP['Initialized'] == False:
            PARAMETER_OPERATION_DISPATCHER_OP[ParameterHandlerOperation.INSERT] = self.insert_parameter
            PARAMETER_OPERATION_DISPATCHER_OP[ParameterHandlerOperation.DELETE] = self.delete_parameter
            PARAMETER_OPERATION_DISPATCHER_OP[ParameterHandlerOperation.UPDATE] = self.update_parameter
            PARAMETER_OPERATION_DISPATCHER_OP[ParameterHandlerOperation.SELECT] = self.select_parameter
            PARAMETER_OPERATION_DISPATCHER_OP['Initialized'] = True
        return PARAMETER_OPERATION_DISPATCHER_OP[pkg['operation_type']](dic, pkg)

    def model_parameter_handler(self, pkg):
        return self.main_operation_handler(self.model_parameters, pkg)

    def data_parameter_handler(self, pkg):
        return self.main_operation_handler(self.data_parameters, pkg)

    def training_parameter_handler(self, pkg):
        return self.main_operation_handler(self.training_parameters, pkg)

    def miscellaneous_parameter_handler(self, pkg):
        return self.main_operation_handler(self.miscellaneous_parameters, pkg)

    def main_parameter_handler(self, pkg:dict):
        if PARAMETER_OPERATION_DISPATCHER_THEME['Initialized'] == False:
            PARAMETER_OPERATION_DISPATCHER_THEME[ParameterType.MODEL] = self.model_parameter_handler
            PARAMETER_OPERATION_DISPATCHER_THEME[ParameterType.DATA] = self.data_parameter_handler
            PARAMETER_OPERATION_DISPATCHER_THEME[ParameterType.TRANINING] = self.training_parameter_handler
            PARAMETER_OPERATION_DISPATCHER_THEME[ParameterType.MISCELLANEOUS] = self.miscellaneous_parameter_handler
            PARAMETER_OPERATION_DISPATCHER_THEME['Initialized'] = True
        try:
            Logger.get_logger().info("Checking Validation of parameter package...")
            if not self.pkg_validation(pkg):
                Logger.get_logger().error("Parameter package does not pass validtion check, your parameter may not be stored successfully !")
        except Exception as e:
            Logger.get_logger().fatal("Exception occured while doing validation check for parameter package.")
            if DEV_MODE == DevelopMode.DEBUG:
                raise Exception("As you are using DEBUG mode, this exception occured, please check context and fix it, or you can mute it by switching to RELEASE mode in CommonDefine.py")
        PARAMETER_OPERATION_DISPATCHER_THEME[pkg['parameter_type']](pkg)
    

    


if __name__ == '__main__':
    x = ParameterWatcher()
    pkg1 = {'parameter_type': ParameterType.MODEL, 'operation_type': ParameterHandlerOperation.INSERT}
    pkg2 = {'parameter_type': ParameterType.DATA, 'operation_type': ParameterHandlerOperation.DELETE}
    pkg3 = {'parameter_type': ParameterType.TRANINING, 'operation_type': ParameterHandlerOperation.UPDATE}
    pkg4 = {'parameter_type': ParameterType.MISCELLANEOUS, 'operation_type': ParameterHandlerOperation.SELECT}
    pkgs = [pkg1, pkg2, pkg3, pkg4]
    for pkg in pkgs:
        x.main_parameter_handler(pkg)