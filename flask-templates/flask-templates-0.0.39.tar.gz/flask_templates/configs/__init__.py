import time
import os
import re
from flask_templates.common.utils import read_yaml, iter_change, mix_change,replace_flat_dict,flat_collect
from collections import OrderedDict

# 基础配置文件名
before_config_filename = 'bootstrap'
base_config_filename = 'application'
# 基础配置路径
init_resource_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'flask_templates', 'resource'))
# 初始配置文件路径
before_env_path = os.path.abspath(os.path.join(init_resource_path, before_config_filename + '.yaml'))
current_env_path = os.path.abspath(os.path.join(init_resource_path, base_config_filename + '.yaml'))
# 基础配置
BEFORE_CONFIG = read_yaml(before_env_path)
BASE_CONFIG = read_yaml(current_env_path)
FINAL_SETTING = {}


def config_update(src_config=BASE_CONFIG, resource_path=None, setting={}, final_setting={}, call_fix=None,
                  src_config_filename=base_config_filename):
    extra_config_dict = dict()
    based_project_path = None
    if resource_path and os.path.exists(resource_path):

        for file in os.listdir(resource_path):
            file_path = os.path.join(resource_path, file)
            if os.path.isdir(file_path):
                continue
            filename = file.rsplit(".yaml", 1)[0]
            if filename == src_config_filename:
                based_project_path = file_path
            elif filename.startswith(src_config_filename + "_"):
                extra_config_dict[filename] = file_path
    # 本地配置文件（对应环境）
    base_project_config = read_yaml(based_project_path)
    mix_change(src_config, base_project_config)
    # 本地配置文件（对应环境）
    env = setting.get("env", src_config.get("env"))
    if env:
        extra_project_config = read_yaml(extra_config_dict.get(src_config_filename + '_' + env))
        mix_change(src_config, extra_project_config)
    # 配置替换,来自服务器的配置可以在这步生效
    mix_change(src_config, setting)
    # 环境变量
    iter_change(src_config, os.environ)
    # 最终配置替换
    FINAL_SETTING.update(final_setting)
    mix_change(src_config, FINAL_SETTING)
    # fix callback
    if call_fix:
        [x() for x in call_fix]
    return src_config


def config_replace(config):
    flat_dict = {}
    flat_collect(config, flat_dict=flat_dict)
    for key in flat_dict:
        replace_flat_dict(key, flat_dict[key]['value'], flat_dict[key]['relative_map'], flat_dict)
    iter_change(config, {k: v['value'] for k, v in flat_dict.items()}, sep=".")


if __name__ == "__main__":
    print(BASE_CONFIG)
    print(config_replace(BASE_CONFIG))