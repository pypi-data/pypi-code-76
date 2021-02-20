import json
import os
import time

from multiprocessing import Process, Queue
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

def handle_args_parser_params(args):
    # print(args._get_kwargs())
    arg_parse_dict = {'parameter_type': ParameterType.MISCELLANEOUS, 'operation_type': ParameterHandlerOperation.INSERT}
    arg_parse_dict['insert_keys'] = []
    for kwarg in args._get_kwargs():
        arg_parse_dict[kwarg[0]] = arg_parse_dict[kwarg[1]]
        arg_parse_dict['insert_keys'].append(kwarg[0])
    return arg_parse_dict

class ParameterWatcher(object):

    @classmethod
    def save_to_file(cls, save_path='./params'):
        while True:
            # if cls.WATCHER_QUEUE.empty():
            #     Logger.get_logger().warning("Empty queue, skipping this round...")
            #     time.sleep(2)
            #     continue
            watcher = cls.WATCHER_QUEUE.get()
            whole_data = dict()
            whole_data['name'] = watcher.name
            whole_data['description'] = watcher.description
            whole_data['model_parameters'] = watcher.model_parameters
            whole_data['training_parameters'] = watcher.training_parameters
            whole_data['data_parameters'] = watcher.data_parameters
            whole_data['miscellaneous_parameters'] = watcher.data_parameters
            whole_data['models'] = watcher.models
            whole_data['results'] = watcher.results
            hash_code = get_md5_hash(whole_data.__str__())
            whole_data['time'] = watcher.time
            whole_data['id'] = watcher.id
            json_str = json.dumps(whole_data)
            name = watcher.name + '_' + hash_code + '_' + watcher.time
            os.makedirs(save_path, exist_ok=True)
            Logger.get_logger().debug("Saving json str {}".format(json_str))
            with open(save_path + '/{}.json'.format(name), 'w') as f:
                f.write(json_str)
            
    @classmethod
    def run_save(cls):
        if hasattr(cls, 'save_proc'):
            Logger.get_logger().warning("Already have one saving process...")
            return False
        Logger.get_logger().info("Starting saving process...")
        cls.save_proc = Process(target=cls.save_to_file)
        # save_proc.daemon = True 
        # Cannot set save process to daemon, otherwise save process will interupt once main thread exits.
        cls.save_proc.start()
        return True
    
    @classmethod
    def terminate_save_proc(cls):
        if cls.save_proc:
            Logger.get_logger().warning("Saving process will terminate in 5s...")
            time.sleep(5)
            while not cls.WATCHER_QUEUE.empty():
                Logger.get_logger().warning("Queue is not empty, waiting save_proc to finish remain queue tasks")
                time.sleep(2)
            cls.save_proc.terminate()
            Logger.get_logger().info("Closing saving process...")
            return True
        else:
            Logger.get_logger().warning("No saving process can be terminated...")
            return False
    
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'WATCHER_QUEUE'):
            cls.WATCHER_QUEUE = Queue()
            cls.run_save()
        return super().__new__(cls)

    def __init__(self, name):
        self.model_parameters = dict()
        self.training_parameters = dict()
        self.miscellaneous_parameters = dict()
        self.data_parameters = dict()
        self.models = dict()
        self.results = dict()
        self.id = get_md5_hash(name + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = name
        self.description = name

    def insert_parameter(self, dic, pkg):
        Logger.get_logger().debug("Inserting parameter package.")
        for key in pkg['insert_keys']:
            if key not in NECESSARY_KEYS:
                dic[key] = pkg[key]

    def delete_parameter(self, dic, pkg):
        Logger.get_logger().debug("Deleting parameter package.")
        for key in pkg['delete_keys']:
            if key not in NECESSARY_KEYS:
                dic.pop(key)

    def update_parameter(self, dic, pkg):
        Logger.get_logger().debug("Updating parameter package.")
        for key in pkg['update_keys']:
            if key not in NECESSARY_KEYS:
                dic[key] = pkg[key]
        

    def select_parameter(self, dic, pkg):
        Logger.get_logger().debug("Selecting parameter package.")
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
            Logger.get_logger().debug("Checking Validation of parameter package...")
            if not self.pkg_validation(pkg):
                Logger.get_logger().error("Parameter package does not pass validtion check, your parameter may not be stored successfully !")
        except Exception as e:
            Logger.get_logger().fatal("Exception occured while doing validation check for parameter package.")
            if DEV_MODE == DevelopMode.DEBUG:
                raise Exception("As you are using DEBUG mode, this exception occured, please check context and fix it, or you can mute it by switching to RELEASE mode in CommonDefine.py")
        PARAMETER_OPERATION_DISPATCHER_THEME[pkg['parameter_type']](pkg)
        ParameterWatcher.WATCHER_QUEUE.put(self, block=False)


if __name__ == '__main__':
    x = ParameterWatcher('test')
    pkgs1 = [{'parameter_type': ParameterType.MODEL, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    pkgs2 = [{'parameter_type': ParameterType.DATA, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    pkgs3 = [{'parameter_type': ParameterType.TRANINING, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    for pkgs in [pkgs1, pkgs2, pkgs3]:
        for pkg in pkgs:
            x.main_parameter_handler(pkg)
    # time.sleep(5)
    ParameterWatcher.terminate_save_proc()