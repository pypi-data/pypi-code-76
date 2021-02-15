import itertools
import numbers
import gc

from ..exception import (AmbiguousSearchSpaceException,
                        RunException, CleanupException)
from ..run.execute import execute_run
from .search_info import insert_metrics_into_best_so_far
from ..const import DEF_KEY_VARIABLE_DICT, DEF_KEY_CLEANUP_FUNCTION
from .special_entries import TUPLE_KEY, unsearchable_run_entry

_DEF_KEY_VARIABLE_TOKEN = '__variables__'

def possible_values(obj):
    """Returns a list of possible values this parameter object can take.

    This is used to compute all possible combinations of key:value pairs in a
    dictionary where elements of lists are taken to be possible, exclusive
    values.

    More specifically:
        - If a dictionary is given, a list of dictionaries is returned where
          entries are computed as follows:
              for every mapping of a key <k> to a list <l> in the input
              dictionary and for every element <e> of <l>, each entry
              dictionary in the output list has a mapping from <k> to <e>
        - If a list is given, it is returned with every dictionary entry turned
          into entries from a list resulting from the procedure described in
          the previous point.
        - Any other object is returned as is.

    In practice, this allows to `unpack` a nested dictionary with lists
    defining possible values of parameters and obtain a list with a single
    combination of parameters for each element.

    For example:
        Turns a complex, nested dictionary of possible hyperparameters
        {
            'model': ['vgg16',
                      {'name': 'perceptron',
                       'hidden_size': [20, 10]
                       }],
            'optimizer':     [
                {
                    'function': 'Adagrad',
                    'lr': 4e-05
                },
                {
                    'function': 'RMSprop',
                    'lr': [1e-2, 1e-4],
                    'momentum': 1e-2
                }
            ]
        }
        into a list of dictionaries with all possible value assignments
        [{'model': 'vgg16', 'optimizer': {'function': 'Adagrad', 'lr': 4e-05}},
         {'model': 'vgg16',
          'optimizer': {'function': 'RMSprop', 'lr': 0.01, 'momentum': 0.01}},
         {'model': 'vgg16',
          'optimizer': {'function': 'RMSprop', 'lr': 0.0001, 'momentum': 0.01}},
         {'model': {'hidden_size': 20, 'name': 'perceptron'},
          'optimizer': {'function': 'Adagrad', 'lr': 4e-05}},
         {'model': {'hidden_size': 20, 'name': 'perceptron'},
          'optimizer': {'function': 'RMSprop', 'lr': 0.01, 'momentum': 0.01}},
         {'model': {'hidden_size': 20, 'name': 'perceptron'},
          'optimizer': {'function': 'RMSprop', 'lr': 0.0001, 'momentum': 0.01}},
         {'model': {'hidden_size': 10, 'name': 'perceptron'},
          'optimizer': {'function': 'Adagrad', 'lr': 4e-05}},
         {'model': {'hidden_size': 10, 'name': 'perceptron'},
          'optimizer': {'function': 'RMSprop', 'lr': 0.01, 'momentum': 0.01}},
         {'model': {'hidden_size': 10, 'name': 'perceptron'},
          'optimizer': {'function': 'RMSprop', 'lr': 0.0001, 'momentum': 0.01}}]
    """
    if type(obj) == list:
        out_list = []
        for item in obj:
            if type(item) == list:
                raise AmbiguousSearchSpaceException(
                    'Nested lists are ambiguous. Use {"__tuple__": [...]} instead.')
            elif type(item) == dict:
                out_list.extend(possible_values(item))
            else:
                out_list.append(item)
        return out_list
    elif type(obj) == dict:
        if unsearchable_run_entry(obj):
            return [obj]
        if TUPLE_KEY in obj:
            possible_values_list = [
                possible_values(item) for item in obj[TUPLE_KEY]
            ]
            out_list = [tuple(possibility)
                        for possibility in itertools.product(*possible_values_list)]
            return out_list
        args_order = sorted(obj.keys())
        ordered_list_of_arg_lists = [possible_values(obj[arg])
                                     for arg in args_order]
        arg_combinations = [{param: combination[idx] for
                         (idx, param) in enumerate(args_order)}
                    for combination in itertools.product(*ordered_list_of_arg_lists)]
        return arg_combinations
    else:
        return [obj]

def define_gridsearch_runs(gridsearch_dict):
    static_params = gridsearch_dict.get('static_params', {})
    execute_function = gridsearch_dict['execute_function']
    experiment_name = gridsearch_dict['experiment_name']
    if DEF_KEY_VARIABLE_DICT in gridsearch_dict:
        gridsearch_dict['params'][
            _DEF_KEY_VARIABLE_TOKEN] = gridsearch_dict[DEF_KEY_VARIABLE_DICT]
    possible_params = possible_values(gridsearch_dict['params'])
    runs = []
    for params in possible_params:
        variables = None
        if _DEF_KEY_VARIABLE_TOKEN in params:
            variables = params[_DEF_KEY_VARIABLE_TOKEN]
            del params[_DEF_KEY_VARIABLE_TOKEN]
        run = {
            "mode": "run",
            "execute_function": execute_function,
            "experiment_name": experiment_name,
            "params": {
                **params, **static_params
            }
        }
        if variables is not None:
            run[DEF_KEY_VARIABLE_DICT] = variables
        if DEF_KEY_CLEANUP_FUNCTION in gridsearch_dict:
            run[DEF_KEY_CLEANUP_FUNCTION] = gridsearch_dict[DEF_KEY_CLEANUP_FUNCTION]
        runs.append(run)
    return runs

def execute_gridsearch(config, env):
    runs = define_gridsearch_runs(config)
    runs_per_configuration = config.get('search_params', {}).get('runs_per_configuration', 1)
    # FIXME: Document best_so_far tracking
    best_so_far_to_remember = config.get('search_params', {}).get('best_so_far_to_remember', 1)
    best_so_far = {'__to_remember__': best_so_far_to_remember}
    for run in runs:
        for n in range(runs_per_configuration):
            gc.collect()
            search_info = {'best_so_far': best_so_far}
            try:
                output = execute_run(run, env, search_info,
                                     search_config=config)
                if isinstance(output, numbers.Number):
                    metrics = {'output': output}
                    insert_metrics_into_best_so_far(best_so_far,
                                                    metrics,
                                                    best_so_far_to_remember)
                elif isinstance(output, dict):
                    insert_metrics_into_best_so_far(best_so_far,
                                                    output,
                                                    best_so_far_to_remember)
            except (RunException, CleanupException):
                print("Run or cleanup failed. Continuing search...")

