# Handles install routine - `amz install`
import subprocess as sp
import os
import shutil
from itertools import zip_longest

from amz.loading import Loading
import amz.meta as meta


# Helper func to install apt, py2, py3 deps
def std_deps(dep_type, filepath, verbose=False, prestr=''):

    # Validate type
    if dep_type not in ['apt', 'py2', 'py3']:
        print('Dependency type not among apt/py2/py3')
        print('Exiting...')
        return

    # list command
    list_cmd = {'apt': 'apt list --installed', 'py2': 'python2 -m pip list', 'py3': 'python3 -m pip list'}

    # Install command before pkgname
    install_cmd = {
        'apt': 'sudo apt --yes install',
        'py2': 'python2 -m pip install --user',
        'py3': 'python3 -m pip install --user'
    }

    filepath_display = filepath
    dep_list = []
    exist_list = []

    if isinstance(filepath, str):
        try:
            if os.path.exists(filepath):
                if len(filepath) > 30:
                    filepath_display = f'...{filepath[-25:]}'
            else:
                print(f'{filepath} - file does not exist')
                print('Exiting...')
                return
        except:
            return

        dep_list = open(filepath, 'r').read().split('\n')
        # Refine Lists not to contain comments(#) or empty lines
        dep_list = [pkg for pkg in dep_list if pkg != '' and '#' not in pkg]

    if isinstance(filepath, list):

        dep_list = filepath

    l = Loading(
        input_str=
        f"Installing {dep_type} dependencies {f'from - {filepath_display}' if isinstance(filepath, str) else ''}",
        input_prestr=prestr)
    l.end(-2)

    p0 = sp.run(list_cmd[dep_type], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    exist_list = [x.split("/" if dep_type == 'apt' else " ")[0].lower() for x in p0.stdout.decode().split('\n')]

    for package in dep_list:
        if package.lower() in exist_list:
            if not verbose:
                l.chain(f'{package} already installed', prestr + '\t')
                l.end(0)
            elif verbose:
                print(f'{package} already installed')
        elif package.lower() not in exist_list:
            if not verbose:
                l.chain(f'{package}', prestr + '\t')
            p = sp.run(f'{install_cmd[dep_type]} {package}',
                       shell=True,
                       stdout=(None if verbose else sp.PIPE),
                       stderr=(None if verbose else sp.PIPE))
            if not verbose:
                l.end(p.returncode)


def script(filepath, input_args, verbose=False, forced=False, mode='install'):
    # Validate the script
    if not meta.validate_script(filepath):
        print(f'Invalid Installer - {filepath}')
        print('Exiting...')
        return
    # Load the script meta and install instructions
    script_meta = meta.get_yaml_config(filepath, ['meta'])
    script_install = meta.get_yaml_config(filepath, [mode])
    # Parse args
    args_exist = "args" in list(script_meta.keys())
    sub_map = []
    sub_map_key = []
    if args_exist:
        arg_dict = script_meta["args"]
        available_args = list(arg_dict.keys())
        if len(input_args) > len(available_args):
            print('More number of args given than possible')
            print('Exiting...')
            return
        # Create substitution map
        sub_map = [
            (f"[({key})]",
             arg_dict[key][arg] if arg is not None and arg in list(arg_dict[key].keys()) else arg_dict[key]['default'])
            for key, arg in zip_longest(available_args, input_args)
        ]
        sub_map_key = [(f"[({key}.key)]", arg if arg is not None and arg in list(arg_dict[key].keys()) else 'default')
                       for key, arg in zip_longest(available_args, input_args)]
    # Handle Temp Dir
    CUR_DIR = os.getcwd()
    TMP_DIR = f"{os.environ['HOME']}/.tmp-amz-{script_meta['name']}"
    if script_meta["temp_dir"] and mode in ['install', 'update']:
        # remove if it exists
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)
        os.mkdir(TMP_DIR)
        os.chdir(TMP_DIR)
    # Check if installed
    p0 = sp.run(script_meta["check"], shell=True, stderr=sp.PIPE, stdout=sp.PIPE)
    if p0.stdout.decode() == 'true\n' and not forced and mode == 'install':
        l = Loading(f"Already installed {script_meta['name']}")
        l.end(0)
        return
    if p0.stdout.decode() == 'false\n' and mode in ['update', 'remove']:
        l = Loading(f"{script_meta['name']} not installed to {mode}")
        l.end(0)
        return
    # Start Display
    pc_form = {'install': 'Installing', 'update': 'Updating', 'remove': 'Removing'}
    l = Loading(f"{'(FORCED) ' if forced else ''}{pc_form[mode]} {script_meta['name']}")
    l.end(-2)
    # Install deps
    if 'deps' in list(script_meta.keys()):
        dep_keys = list(script_meta['deps'].keys())
        for dep_type in dep_keys:
            std_deps(dep_type, script_meta['deps'][dep_type], verbose, '\t')
    # Install steps
    for section in list(script_install.keys()):
        # Check if section is blocking
        is_blocking = '!!!' in section
        disp_title = section.replace('!!!', '')
        ## Perform substitution for display title
        if args_exist:
            for key, val in sub_map + sub_map_key:
                disp_title = disp_title.replace(key, val)
        # Anim start
        if not verbose:
            l.chain(f'{disp_title}', '\t')
        # Final return code
        retcode = 0
        # Loop through commands under section
        for cmd in script_install[section]:
            ## Perform substitution for each commands
            if args_exist:
                for key, val in sub_map:
                    cmd = cmd.replace(key, val)
            # Execute via subprocess
            p = sp.run(cmd, shell=True, stdout=(None if verbose else sp.PIPE), stderr=(None if verbose else sp.PIPE))
            retcode += p.returncode
            # If blocking section, close if retcode is not 0
            if retcode != 0 and is_blocking:
                if not verbose:
                    l.end(retcode)
                return
        # Anim end
        if not verbose:
            l.end(retcode)
    # Clean Up and Back to Cur Dir
    if script_meta["temp_dir"] and mode in ['install', 'update']:
        shutil.rmtree(TMP_DIR)
        os.chdir(CUR_DIR)
