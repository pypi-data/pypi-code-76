from dubhe.dataset import dataset
from dubhe.service import context
from dubhe.utils import config
from dubhe.service import dataset as dataset_service
from dubhe.service import out_dataset as out_dataset_service
import os
import importlib
import sys
import typing
import inspect
import random
import string
import shutil


def _get_dubhe_manifest(home: str) -> str:
    return os.path.join(home, "DubheManifest.json")


def _is_image_home(home: str) -> bool:
    mainfest = _get_dubhe_manifest(home)
    if os.path.exists(mainfest) and os.path.isfile(mainfest):
        return True
    else:
        return False


def _find_pipelines(home: str) -> typing.List[typing.Tuple]:
    base = os.path.join(home, 'src')

    sys.path.insert(0, base)

    pipelines = []
    files = os.listdir(base)
    for filename in files:
        filename = os.path.join(base, filename)
        if filename[-3:] != '.py' or not os.path.isfile(filename):
            continue

        _, module_name_with_ext = os.path.split(filename)
        module_name, _ = os.path.splitext(module_name_with_ext)
        module_spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        for name in dir(module):
            if name.startswith('__'):
                continue

            obj = module.__getattribute__(name)
            if hasattr(obj, '_is_pipeline_func'):
                pipelines.append((module, name))
    sys.path.remove(base)
    return pipelines


def _find_entrance(pipelines: typing.List[typing.Tuple]) -> typing.List[typing.Tuple]:
    entrances = []

    for pipe in pipelines:
        module = pipe[0]
        name = pipe[1]
        obj = module.__getattribute__(name)
        for _, function in inspect.getmembers(
                obj,
                predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x),
        ):
            func_type = None
            if hasattr(function, "_is_train_func"):
                func_type = 'train'
            elif hasattr(function, "_is_predict_func"):
                func_type = 'predict'

            if func_type is not None:
                algorithm_id = getattr(function, "_algorithm_id")
                is_main = getattr(function, "_is_main")
                entrances.append((module, name, func_type, algorithm_id, is_main, function))

    return entrances


def _invoke_func(func: typing.Callable, algorithm_id: str, input_train: dataset.Dataset, input_valid: dataset.Dataset):
    # todo use cli parameters to build context, maybe need move all functions in this file into pipeline.py or a mgr
    #  class

    rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

    model_path = os.path.join(config.HOME, rand, "model")
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    cache_path = os.path.join(config.HOME, rand, "cache")
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    # todo, download model cache to path by mode

    input_train_ds = dataset_service.Dataset(input_train)
    input_valid_ds = dataset_service.Dataset(input_valid)

    out_ds = out_dataset_service.OutDataset()

    ctx = context.ContextBuilder(None).addStr(context.ContextKey.KEY_ALGORITHM_ID, algorithm_id) \
        .addInt(context.ContextKey.KEY_EPOCH_COUNT, 50) \
        .addDataset(context.ContextKey.KEY_TRAIN_DATASET, input_train_ds) \
        .addDataset(context.ContextKey.KEY_VALIDATION_DATASET, input_valid_ds) \
        .setModelDir(model_path) \
        .setCacheDir(cache_path) \
        .setOutDataset(out_ds) \
        .build()
    func(ctx)

    out_ds.flush()

    # todo, upload model cache to path by mode
    shutil.rmtree(os.path.join(config.HOME, rand))


def run_train(home: str, method: str, algorithm_id: str, input_train: dataset.Dataset,
              input_valid: dataset.Dataset) -> str:
    if not _is_image_home(home):
        return f'pwd {home} is not a dubhe image home'

    pipelines = _find_pipelines(home)
    entrances = _find_entrance(pipelines)
    for entrance in entrances:
        func_type = entrance[2]
        entrance_algorithm_id = entrance[3]
        is_main = entrance[4]

        if func_type == method:
            if algorithm_id == entrance_algorithm_id or (algorithm_id is None and is_main):
                module = entrance[0]
                name = entrance[1]
                obj = module.__getattribute__(name)
                function = entrance[5]
                user_func = function.__get__(obj)
                _invoke_func(user_func, algorithm_id, input_train, input_valid)
                break


def run_predict(home: str, method: str, algorithm_id: str, input_test: dataset.Dataset,
                data_out: dataset.Dataset) -> str:
    pass
