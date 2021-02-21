import os
import sys
import logging
import importlib
import unitorch
from unitorch import core_configure_parser, core_task, AUTO_CONFIG_FROM_HUB_DICT
from unitorch.utils.hf import hf_cached_path
import fire

config_files_in_repo = os.walk(os.path.join(os.path.dirname(__file__), "../config"))
CONFIG_FROM_REPO = dict()
for root_dir, dirs, files in config_files_in_repo:
    for file in files:
        if file.endswith(".ini"):
            config_path = os.path.normpath(os.path.join(root_dir, file))
            config_name = config_path[:-4]
            config_name = config_name[config_name.index('config'):]
            CONFIG_FROM_REPO[config_name] = config_path


TEMPLATE_FROM_REPO = dict()
TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "../templates")]
for template_dir in TEMPLATE_DIRS:
    templates = os.listdir(template_dir)
    templates = [os.path.normpath(os.path.join(template_dir, template)) for template in templates]
    templates = list(filter(os.path.isdir, templates))
    for template in templates:
        template_path = os.path.normpath(os.path.join(template_dir, template))
        template_name = template_path[template_path.index('templates'):]
        TEMPLATE_FROM_REPO[template_name] = template_path

AUTO_CONFIG_DICT = {
    **AUTO_CONFIG_FROM_HUB_DICT,
    **CONFIG_FROM_REPO,
    **TEMPLATE_FROM_REPO,
}

logging.info(AUTO_CONFIG_DICT)


def train(cfg_path_or_dir, **kwargs):
    config_file = kwargs.pop("config_file", "config.ini")
    assert cfg_path_or_dir in AUTO_CONFIG_DICT or os.path.exists(cfg_path_or_dir)
    if cfg_path_or_dir in AUTO_CONFIG_DICT:
        cfg_path = AUTO_CONFIG_DICT[cfg_path_or_dir]

    if os.path.isdir(cfg_path_or_dir):
        cfg_path = os.path.join(cfg_path_or_dir, config_file)
        sys.path.insert(0, cfg_path_or_dir)
        for f in os.listdir(cfg_path_or_dir):
            fpath = os.path.join(cfg_path_or_dir, f)
            if (
                not f.startswith("_")
                and not f.startswith(".")
                and (f.endswith(".py") or os.path.isdir(fpath))
            ):
                fname = f[:-3] if f.endswith(".py") else f
                module = importlib.import_module(f"{fname}")

    elif os.path.isfile(cfg_path_or_dir):
        cfg_path = cfg_path_or_dir

    cfg_path = hf_cached_path(cfg_path)

    params = []
    for k, v in kwargs.items():
        if k.count("@") > 0:
            k0 = k.split("@")[0]
            k1 = k.split("@")[1]
        else:
            k0 = "core/auto"
            k1 = k
        params.append((k0, k1, v))

    cfg = core_configure_parser(cfg_path, params)

    # init core libs
    unitorch.init_core_group(cfg)

    task_type = cfg.getdefault("core/auto", "task_type", None)
    assert task_type is not None

    if task_type in unitorch.core_task:
        unitorch.core_task.get(task_type).train()
    else:
        raise f"can't find the task {task_type}"


def cli_main():
    fire.Fire(train)


if __name__ == "__main__":
    fire.Fire(train)
