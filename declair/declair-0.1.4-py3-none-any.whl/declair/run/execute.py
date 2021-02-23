from copy import deepcopy
import traceback
import inspect
import gc
import os
import multiprocessing
import sys
from queue import Empty
from time import sleep

import wrapt
from sacred import Experiment
from tblib import pickling_support

from ..const import (DEF_KEY_ENV_PARAMS, DEF_KEY_SEARCH_INFO,
                     DEF_KEY_EXECUTE_FUNCTION, DEF_KEY_CLEANUP_FUNCTION,
                     DEF_KEY_EXPERIMENT_NAME, DEF_STORED_RUN_CONFIG_NAME,
                     DEF_STORED_SEARCH_CONFIG_NAME, DEF_KEY_VARIABLE_DICT)
from .type import insert_type
from .env import insert_env
from .call import insert_call_results
from .variables import insert_var, insert_var_instance
from .sources import find_sources
from ..serialization import serialize_type_dict
from ..results import append_observers_to_experiment, add_artifact_string
from ..exception import (RunException, CleanupException,
                         InvalidConfigException,
                         InvalidExecuteFunctionException)

# There will be two configuration dictionaries:
#  - One with no initialized objects, which can be later executed as a run on
#    its own
#  - One with initialized entries, which will be used directly as the input to
#    the function
# The reason for this distinction is that, depending on the underlying storage,
# Sacred has a size limit on configs it can store. For MongoDB, which is the
# most handy Sacred backend, this limit is a bit more than 10mb, which can be
# insufficient for e.g. initialized models.
def _config_to_store(config, env, search_info):
    config = deepcopy(config)
    config[DEF_KEY_ENV_PARAMS] = env.get_dict()
    if DEF_KEY_SEARCH_INFO not in config:
        config[DEF_KEY_SEARCH_INFO] = {} if not search_info else search_info
    return config

def _config_to_execute(config, env):
    config = deepcopy(config)
    config = insert_type(config)
    config = insert_env(config, env)
    # TODO: Raise exception if variable entries occur in config[variables],
    #       since that implies recursion which isn't the main goal here
    config = insert_var(config, config.get(DEF_KEY_VARIABLE_DICT, {}))
    config = insert_call_results(config)
    config = insert_var_instance(config, config.get(DEF_KEY_VARIABLE_DICT, {}))
    return config

def _clean_kwargs(kwargs, func):
    # returns a dict with all arguments removed which aren't actual kwargs of
    # the function, so if **clean_kwargs is given as an argument it doesn't
    # throw an exception
    sig_params = inspect.signature(func).parameters
    clean_kwargs = {key: val
                    for (key, val) in kwargs.items()
                    if key in sig_params}
    return clean_kwargs

def _default_basedir(config_to_execute):
    return os.path.dirname(
        inspect.getfile(config_to_execute[DEF_KEY_EXECUTE_FUNCTION])
    )

# TODO: Document cleanup
def _get_cleanup_func(config_to_execute):
    if DEF_KEY_CLEANUP_FUNCTION in config_to_execute:
        # Detect which keyword arguments are allowed so there isn't a type
        # error complaining about too many args
        # This is so the cleanup_function has an equivalent API to the
        # execution_function
        clean_func = config_to_execute[DEF_KEY_CLEANUP_FUNCTION]
        clean_kwargs = _clean_kwargs(config_to_execute, clean_func)
        del config_to_execute
        def _cleanup():
            clean_func(**clean_kwargs)
            gc.collect()
    else:
        def _cleanup():
            gc.collect()
    return _cleanup

def _clean_result(run_result):
    # If the run result contains tensors with a computation graph, it might
    # cause a memory leak after many runs, since result values are kept in e.g.
    # hyperopt search. Thus, we turn them into floats
    try:
        return float(run_result)
    except TypeError:
        if not isinstance(run_result, dict):
            raise InvalidExecuteFunctionException(
                "Execute function must return either scalar or dictionary of <metric name>:<scalar value>, but returns {}".format(type(run_result).__name__))
        out_result = {}
        for key, val in run_result.items():
            try:
                out_result[key] = float(val)
            except TypeError:
                raise InvalidExecuteFunctionException(
                    "Return type of values in the output dictionary must be numeric, but key {} has type {}".format(key, type(val)))
        return out_result

def _execute_run(config, env, search_info=None, base_dir=None,
                search_config=None, perform_cleanup=True):
    config_to_store = _config_to_store(config, env, search_info)
    config_to_execute = _config_to_execute(config, env)

    # base_dir influences Sacred's source discovery
    if base_dir is None:
        base_dir = _default_basedir(config_to_execute)
    sources = find_sources(config_to_store)

    cleanup = _get_cleanup_func(config_to_execute)

    @wrapt.decorator
    def _config_insertion_wrapper(wrapped, instance, args, kwargs):
        # Here, Sacred provides us with uninitialized configs. Now we can
        # replace them by the actual initialized configs to be given as
        # arguments to the function.
        #
        # There might be more keys in the `config` dictionary than in the
        # function signature, and providing them all via `**kwargs` will call
        # an exception. Sacred has already filtered them out based on the
        # funtion signature in the `kwargs` we are given, so we can just filter
        # the entries of `config_to_execute` we need.
        #
        # Lastly, there might be extra Sacred related keys like `_run` in
        # `kwargs`, so we need to filter them out as well.
        true_declair_kwargs = {
            key: config_to_execute[key] for key in kwargs if key in config_to_execute
        }
        true_sacred_kwargs = {
            key: kwargs[key] for key in kwargs if key not in config_to_execute
        }
        true_kwargs = {
            **true_sacred_kwargs,
            **true_declair_kwargs
        }
        # Note that `args` should be empty anyway.
        return wrapped(**true_kwargs)
    execute_function = _config_insertion_wrapper(config_to_execute[DEF_KEY_EXECUTE_FUNCTION])

    ex = Experiment(name=config_to_execute[DEF_KEY_EXPERIMENT_NAME], base_dir=base_dir)
    for source in sources:
        ex.add_source_file(source)
    ex.main(execute_function)
    ex.add_config(config_to_store)
    ex.pre_run_hook(lambda: add_artifact_string(ex, serialize_type_dict(
        config_to_store, indent=True), DEF_STORED_RUN_CONFIG_NAME))
    if search_config is not None:
        ex.pre_run_hook(lambda: add_artifact_string(ex, serialize_type_dict(
            search_config, indent=True), DEF_STORED_SEARCH_CONFIG_NAME))
    append_observers_to_experiment(ex, env)
    if perform_cleanup:
        try:
            run = ex.run()
        except:
            try:
                cleanup()
            except:
                raise CleanupException()
            raise RunException()
        try:
            cleanup()
        except:
            raise CleanupException()
        return _clean_result(run.result)
    else:
        try:
            run = ex.run()
        except:
            raise RunException()
        return _clean_result(run.result)

def _execute_run_and_put_in_queue(queue, *args, **kwargs):
    try:
        result = _execute_run(*args, **kwargs)
        queue.put(result)
    except Exception as e:
        traceback.print_exc()
        # We want to transfer the exception to the parent process so it can be
        # re-raised with as much information kept as possible. By default,
        # trying to pass sys.exc_info() would just fail because tracebacks
        # aren't picklable. tblib.pickling_support.install lets us overcome
        # that.
        pickling_support.install(e)
        queue.put(sys.exc_info())

def execute_run(config, env, search_info=None, base_dir=None,
                search_config=None):
    if DEF_KEY_EXPERIMENT_NAME not in config:
        raise InvalidConfigException("'experiment_name' field missing and could not be obtained from experiment filename")
    config_to_execute = _config_to_execute(config, env)
    cleanup = _get_cleanup_func(config_to_execute)
    del config_to_execute

    ctx = multiprocessing.get_context('spawn')
    queue = ctx.Queue()

    proc = ctx.Process(
        target=_execute_run_and_put_in_queue,
        args=(queue, config, env),
        kwargs={
            DEF_KEY_SEARCH_INFO: search_info,
            'base_dir': base_dir,
            'search_config': search_config,
            'perform_cleanup': False
        }
    )
    proc.start()
    try:
        while True:
            try:
                output = queue.get_nowait()
                # Check if it's a sys.exc_info output, i.e. exception
                if (isinstance(output, tuple)
                        and len(output) == 3
                        and isinstance(output[0], type)
                        and issubclass(output[0], Exception)):
                    raise output[1].with_traceback(output[2])
                break
            except Empty:
                if not proc.is_alive():
                    if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
                        proc.terminate()
                        proc.close()
                    raise RunException("Run process is dead with no exception (maybe out of memory?)")
                sleep(0.1)
    except KeyboardInterrupt:
        proc.terminate()
        if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
            proc.close()
        raise
    proc.join()
    if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
        proc.terminate()
        proc.close()
    cleanup()
    return output
