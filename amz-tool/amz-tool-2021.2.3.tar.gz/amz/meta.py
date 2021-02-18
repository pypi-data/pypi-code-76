# Handles fetching of meta data
import os
from functools import reduce
from operator import getitem
from itertools import product
import subprocess as sp
import yaml


def update_line_in_file(replace_containing, replace_with, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines_upd = [f"{replace_with}\n" if replace_containing in l else l for l in lines]
    with open(filename, 'w') as file:
        file.write(''.join(lines_upd))


def get_version():
    PKG_DIR = os.path.dirname(__file__)
    v = open(f'{PKG_DIR}/data/VERSION').readlines()[0]
    return v.ljust(10, ' ')


def get_amz_config(key_chain):

    HOME_DIR = os.environ["HOME"]
    AMZ_CONFIG_FILE = HOME_DIR + '/.amz/config/amz-config.yaml'
    try:
        config = yaml.load(open(AMZ_CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return None


def get_yaml_config(filepath, key_chain):

    try:
        config = yaml.load(open(filepath, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return None


def highlight_cmd(cmd):
    return f'\033[90m\033[107m {cmd} \033[0m'


def validate_script(filepath):
    # Open and parse yaml file
    yf = yaml.load(open(filepath), Loader=yaml.FullLoader)
    # Check for 4 sections - Meta, Install, Update, Remove
    if list(yf.keys()).sort() != ['meta', 'install', 'update', 'remove'].sort():
        return False
    # Meta Section
    ## Reqd Keys
    if 'name' not in list(yf['meta'].keys()):
        return False
    if 'check' not in list(yf['meta'].keys()):
        return False
    ## deps keys are known?
    if 'deps' in list(yf['meta'].keys()):
        if not set(yf['meta']['deps'].keys()).issubset(set(['apt', 'py2', 'py3'])):
            return False
    ## args have default keys?
    if 'args' in list(yf['meta'].keys()):
        if not all('default' in val for val in list(yf['meta']['args'].values())):
            return False
    # Install/Update/Remove Section
    for sec in ['install', 'update', 'remove']:
        ## Each dict value is a list of str
        if not all(all(isinstance(cmd, str) for cmd in cmds) for cmds in list(yf[sec].values())):
            return False
    return True


def autocomplete_choices():
    try:
        amz_yaml = ''
        p = sp.run('git rev-parse --show-toplevel', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        # Check if your current repo is recognized as amz
        if p.returncode == 0 and os.path.exists(f'{p.stdout.decode()[:-1]}/amz.yaml'):
            amz_yaml = f'{p.stdout.decode()[:-1]}/amz.yaml'
        else:
            amz_yaml = get_amz_config(['amz_repo_meta', 'amz_repo_config'])
        # Fetch autocomplete options
        auto_yaml = get_yaml_config(amz_yaml, [])
        if auto_yaml is None:
            return None
        choices = list(set(['apt-deps', 'py2-deps', 'py3-deps']) & set(auto_yaml.keys()))
        if 'scripts' in auto_yaml.keys() and auto_yaml['scripts'] is not None:
            choices += list(auto_yaml['scripts'].keys())
            for scr in auto_yaml['scripts'].keys():
                args_avail = get_yaml_config(f'{amz_yaml[:-9]}/{auto_yaml["scripts"][scr]}', ['meta', 'args'])
                if args_avail is not None:
                    arg_list = [list(args_avail[arg].keys())[1:] for arg in list(args_avail.keys())]
                    choices += [f'{scr}.' + '.'.join(opts) for opts in list(product(*arg_list))]
        return choices
    except:
        return None


def substitute_in_file(replace_str, replace_with, filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(replace_str, replace_with)
        with open(filepath, 'w') as file:
            file.write(filedata)
