import gc

from hyperopt import hp, fmin
from hyperopt.pyll.base import scope

from ..serialization import string_to_type
from ..exception import (InvalidConfigException, AmbiguousSearchSpaceException,
                        RunException, CleanupException)
from ..run.execute import _config_to_execute, execute_run
from .search_info import insert_metrics_into_best_so_far
from ..const import (DEF_KEY_VARIABLE_DICT, DEF_KEY_PARAMS, DEF_KEY_SEARCH_PARAMS,
                     DEF_KEY_STATIC_PARAMS, DEF_KEY_EXECUTE_FUNCTION, DEF_KEY_EXPERIMENT_NAME,
                     DEF_KEY_TYPE, DEF_TYPE_RUN, DEF_KEY_CLEANUP_FUNCTION)

from .special_entries import HYPEROPT_KEY, TUPLE_KEY, unsearchable_run_entry

_DEF_KEY_VARIABLE_TOKEN = '__variables__'

def _get_hyperopt_dtype(obj):
    """Returns the expected data type of a hyperopt parameter. Can either be
    `float` or `int`.
    """
    # The user can explicitly define dtype
    if 'dtype' in obj:
        if obj['dtype'] in ['float', 'int']:
            return string_to_type('builtins.{}'.format(obj['dtype']))
        else:
            raise InvalidConfigException(
                "Hyperopt parameter dtype not valid. Must be 'float' or 'int'")
    # otherwise, try to infer it based on if it's one of the possible quantized
    # parameter expressions with an integer step
    # https://github.com/hyperopt/hyperopt/wiki/FMin#21-parameter-expressions
    typename = obj[HYPEROPT_KEY]
    if typename == 'randint':
        return int
    elif typename in [
            'quniform',
            'qloguniform',
            'qnormal',
            'qlognormal']:
        if 'args' in obj:
            # the last argument is q, i.e. step. It really defines the dtype
            q = obj['args'][-1]
        elif 'kwargs' in obj:
            q = obj['kwargs']['q']
        else:
            raise InvalidConfigException(
                "Hyperopt parameter 'args' or 'kwargs' not given")
        return type(q)
    else:
        return float

def _get_hyperopt_dtype_str(obj):
    return _get_hyperopt_dtype(obj).__name__

def _dict_to_hyperopt(obj, root):
    args = obj.get('args', ())
    kwargs = obj.get('kwargs', {})
    type_ = string_to_type("hyperopt.hp.{}".format(obj[HYPEROPT_KEY]))
    dtype_str = _get_hyperopt_dtype_str(obj)
    # "scope" defines the dtype in pyll, the hyperopt probabilistic language
    scope_func = getattr(scope, dtype_str)
    return scope_func(type_(root, *args, **kwargs))

def hyperopt_search_space(obj, root='root'):
    """
    Returns a hyperopt search space constructed from an object.

    Similar to `possible_values`, lists define a choice between disjoint
    options. Unlike `possible_values`, this type of search space can also
    include hyperopt numeric distributions. Hyperopt distributions are defined
    by dictionaries of form
        {'__hp__': <distribution function>, 'args': <args>}
    or
        {'__hp__': <distribution function>, 'kwargs': <kwargs>}
    where the distribution functions, possible args or kwargs can be found
    here:
    https://github.com/hyperopt/hyperopt/wiki/FMin#21-parameter-expressions

    For example, a valid search tree with hyperopt numeric distributions:
        {
            'model': ['vgg16',
                      {'name': 'perceptron',
                       'hidden_size': {'__hp__': 'quniform', 'args': (10, 50, 10)}
                       }],
            'optimizer':     [
                {
                    'function': 'Adagrad',
                    'lr': {'__hp__': 'lognormal', 'kwargs': {'mu': 1, 'sigma': 1}}
                },
                {
                    'function': 'RMSprop',
                    'lr': {'__hp__': 'uniform', 'args': (1e-4, 1e-2)},
                    'momentum': 1e-2
                }
            ]
        }
    """
    if type(obj) == list:
        out_list = []
        for num, item in enumerate(obj):
            if type(item) == list:
                raise AmbiguousSearchSpaceException(
                    'Nested lists are ambiguous. Use {"__tuple__": [...]} instead.')
            elif type(item) == dict:
                out_list.append(hyperopt_search_space(item, root='{}[{}]'.format(root, num)))
            else:
                out_list.append(item)
        return hp.choice(root, out_list)
    elif type(obj) == dict:
        if unsearchable_run_entry(obj):
            return obj
        if HYPEROPT_KEY in obj:
            return _dict_to_hyperopt(obj, root)
        if TUPLE_KEY in obj:
            out_list = []
            for num, item in enumerate(obj[TUPLE_KEY]):
                out_list.append(
                    hyperopt_search_space(item, root='{}/{}'.format(root, num)))
            return out_list
        out_dict = {}
        for key, value in obj.items():
            if type(value) == list or type(value) == dict:
                out_dict[key] = hyperopt_search_space(value, root='{}/{}'.format(root, key))
            else:
                out_dict[key] = value
        return out_dict
    else:
        return obj


def hyperopt_params_to_params(search_space_definition, hyperopt_params, root='root'):
    """
    Returns a parameter dictionary from a hyperopt result dictionary, e.g. from
    the result of hp.fmin, given also the original search space definition
    dictionary.

    For example, a possible optimization result from the search space definition
        {
            'model': ['vgg16',
                      {'name': 'perceptron',
                       'hidden_size': {'__hp__': 'quniform', 'args': (10, 50, 10)}
                       },
                      {'name': 'mlperceptron',
                       'hidden_sizes': {'__tuple__': [
                           {'__hp__': 'quniform', 'args': (10, 50, 10)},
                           {'__hp__': 'quniform', 'args': (10, 30, 10)}
                       ]}}],
            'optimizer':     [
                {
                    'function': 'Adagrad',
                    'lr': {'__hp__': 'lognormal', 'kwargs': {'mu': 1, 'sigma': 1}}
                },
                {
                    'function': 'RMSprop',
                    'lr': {'__hp__': 'uniform', 'args': (1e-4, 1e-2)},
                    'momentum': 1e-2
                }
            ],
            'batch_size': [
                {'__hp__': 'quniform', 'args': (20, 60, 5)},
                {'__hp__': 'quniform', 'args': (400, 440, 5)}
            ]
        }
    is
        {'root/batch_size': 0,
         'root/batch_size[0]': 420.0,
         'root/model': 2,
         'root/model[2]/hidden_sizes/0': 20.0,
         'root/model[2]/hidden_sizes/1': 20.0,
         'root/optimizer': 1,
         'root/optimizer[1]/lr': 0.0022019496801429354}
    which corresponds to a parameter dictionary
        {
            'model': {
                'name': 'mlperceptron', 'hidden_sizes': (20, 20)
            },
            'optimizer': {
                'function': 'Adagrad',
                'lr': 0.0022019496801429354,
                'momentum': 1e-2
            },
            'batch_size': 420
        }
    """
    obj = search_space_definition
    if type(obj) == list:
        if root in hyperopt_params:
            index = hyperopt_params[root]
            return hyperopt_params_to_params(obj[index],
                                             hyperopt_params=hyperopt_params,
                                             root='{}[{}]'.format(root, index))
        else:
            # If a list isn't included in the hyperopt params, then it's
            # excluded from the search and is static
            return obj
    elif type(obj) == dict:
        if unsearchable_run_entry(obj):
            return obj
        if HYPEROPT_KEY in obj:
            dtype = _get_hyperopt_dtype(obj)
            val = dtype(hyperopt_params[root])
            return val
        if TUPLE_KEY in obj:
            out_list = []
            for index, item in enumerate(obj[TUPLE_KEY]):
                out_list.append(
                    hyperopt_params_to_params(item,
                                              hyperopt_params=hyperopt_params,
                                              root='{}/{}'.format(root, index)))
            return tuple(out_list)
        out_dict = {}
        for key, value in obj.items():
            out_dict[key] = hyperopt_params_to_params(value,
                                                      hyperopt_params=hyperopt_params,
                                                      root='{}/{}'.format(root, key))
        return out_dict
    else:
        return obj

def define_run_from_params(params, search_dict):
    static_params = search_dict.get(DEF_KEY_STATIC_PARAMS, {})
    execute_function = search_dict[DEF_KEY_EXECUTE_FUNCTION]
    experiment_name = search_dict[DEF_KEY_EXPERIMENT_NAME]
    variables = None
    if _DEF_KEY_VARIABLE_TOKEN in params:
        variables = params[_DEF_KEY_VARIABLE_TOKEN]
        del params[_DEF_KEY_VARIABLE_TOKEN]
    run_dict = {
        DEF_KEY_TYPE: DEF_TYPE_RUN,
        DEF_KEY_EXECUTE_FUNCTION: execute_function,
        DEF_KEY_EXPERIMENT_NAME: experiment_name,
        DEF_KEY_PARAMS: {
            **params, **static_params
        }
    }
    if variables is not None:
        run_dict[DEF_KEY_VARIABLE_DICT] = variables
    if DEF_KEY_CLEANUP_FUNCTION in search_dict:
        run_dict[DEF_KEY_CLEANUP_FUNCTION] = search_dict[DEF_KEY_CLEANUP_FUNCTION]
    return run_dict

def execute_hyperopt_search(config, env):
    search_params = config.get(DEF_KEY_SEARCH_PARAMS)
    if not search_params:
        raise InvalidConfigException("Please provide search_params in the experiment definition")
    fmin_kwargs = _config_to_execute(search_params.get('fmin_kwargs', {}), env)
    if not fmin_kwargs:
        raise InvalidConfigException("Please provide search_params.fmin_kwargs in the experiment definition")
    opt_params = search_params.get('optimize')
    if not opt_params:
        raise InvalidConfigException("Please provide search_params.optimize in the experiment definition")
    # FIXME: Document best_so_far tracking
    best_so_far_to_remember = config.get('search_params', {}).get('best_so_far_to_remember', 1)
    best_so_far = {'__to_remember__': best_so_far_to_remember}
    opt_type = opt_params.get('type')
    if opt_type is None:
        raise InvalidConfigException("Please provide search_params.optimize.type in the experiment definition (either 'max' or 'min').")
    if opt_type == 'min':
        opt_sign = 1
    elif opt_type == 'max':
        opt_sign = -1
    else:
        raise InvalidConfigException("Optimization type search_params.optimize.type must be max or min")
    opt_target = opt_params.get('target', None)
    def opt_func(run_params):
        gc.collect()
        run_config = define_run_from_params(run_params, config)
        search_info = {'best_so_far': best_so_far}
        try:
            output = execute_run(run_config, env, search_info,
                                 search_config=config)
            if opt_target is None:
                try:
                    opt_val = float(output)
                    metrics = {'output': opt_val}
                    # best_so_far causes a race condition in case this code gets parallelized
                    insert_metrics_into_best_so_far(best_so_far,
                                                    metrics,
                                                    best_so_far_to_remember)
                except TypeError:
                    raise ValueError("Optimization target search_params.optimize.target not given and optimization function output is not numeric.")
            else:
                opt_val = output.get(opt_target, float('nan'))
                insert_metrics_into_best_so_far(best_so_far,
                                                output,
                                                best_so_far_to_remember)
        except (RunException, CleanupException):
            opt_val = float('nan')
            print("Run or cleanup failed. Continuing search...")
        opt_val *= opt_sign
        return opt_val
    if DEF_KEY_VARIABLE_DICT in config:
        config[DEF_KEY_PARAMS][_DEF_KEY_VARIABLE_TOKEN] = config[DEF_KEY_VARIABLE_DICT]
    space = hyperopt_search_space(config[DEF_KEY_PARAMS])
    # We don't necessarily need to write down the best result anywhere now,
    # because it will have been saved by Sacred. We can just search for the top
    # result via Omniboard.
    best = fmin(fn=opt_func,
            space=space, **fmin_kwargs)
