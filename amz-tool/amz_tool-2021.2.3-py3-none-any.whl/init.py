# Defines routine for `amz init`
import os
import getpass
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from configparser import RawConfigParser
import subprocess as sp
import yaml

from amz.loading import Loading
import amz.meta as meta
import amz.install as install

HOME_DIR = os.environ["HOME"]
PKG_DIR = os.path.dirname(__file__)
AMZ_DATA_DIR = HOME_DIR + '/.amz/data'
AMZ_CONFIG_DIR = HOME_DIR + '/.amz/config'


# General Initialization
def amz_gen_init(verbose=False):
    l = Loading("AMZ tool initialization routine")
    l.end(-2)

    # Check for `~/.amz` directory and make one if not there
    l.chain("Checking for `~/.amz` directory", "\t")
    AMZ_DIR_PRESENT = os.path.exists(f"{HOME_DIR}/.amz")
    if not AMZ_DIR_PRESENT:
        os.mkdir(f"{HOME_DIR}/.amz")

    # Copy data folder if contents do not match
    l.chain("Copying data", "\t", 0)
    try:
        copy_tree(f'{PKG_DIR}/data', AMZ_DATA_DIR)
        # Copy if config path doesn't exist
        if not os.path.exists(AMZ_CONFIG_DIR):
            copy_tree(f'{PKG_DIR}/config', AMZ_CONFIG_DIR)
        else:
            # Copy if amz_source.spec change has been detected.
            src_conf_lines = len(open(f'{PKG_DIR}/config/amz_source.sh').readlines())
            dst_conf_lines = len(open(f'{AMZ_CONFIG_DIR}/amz_source.sh').readlines())
            if src_conf_lines is not dst_conf_lines:
                copy_file(f'{PKG_DIR}/config/amz_source.sh', f'{AMZ_CONFIG_DIR}/amz_source.sh')
    except FileExistsError:
        l.end(1)

    # Update version info in amz-config yaml
    try:
        amz_user_config = yaml.load(open(f'{AMZ_CONFIG_DIR}/amz-config.yaml'), Loader=yaml.FullLoader)
        amz_user_config['amz_tool_meta']['version'] = open(f'{AMZ_DATA_DIR}/VERSION').readlines()[0]
        amz_user_config['amz_tool_meta']['user'] = getpass.getuser()
        with open(f'{AMZ_CONFIG_DIR}/amz-config.yaml', 'w') as f:
            yaml.dump(amz_user_config, f)
        meta.update_line_in_file('export AMZ_DATA=', f"export AMZ_DATA={AMZ_DATA_DIR}",
                                 f"{AMZ_CONFIG_DIR}/amz_source.sh")
        meta.update_line_in_file('export AMZ_CONFIG=', f"export AMZ_CONFIG={AMZ_CONFIG_DIR}",
                                 f"{AMZ_CONFIG_DIR}/amz_source.sh")
        # Attempt to update `amz_source.sh` with current AMZ_ROOT environment var
        if "AMZ_ROOT" in os.environ.keys():
            meta.update_line_in_file('export AMZ_ROOT=', f'export AMZ_ROOT={os.environ["AMZ_ROOT"]}',
                                     f'{AMZ_CONFIG_DIR}/amz_source.sh')
    except:
        l.end(1)

    # Turn paths to custom githooks into absolute paths
    try:
        meta.substitute_in_file('AMZ_DATA_DIR', AMZ_DATA_DIR, f'{AMZ_DATA_DIR}/githooks/config/.pre-commit-config.yaml')
    except:
        l.end(1)

    l.end(0)

    # APT Deps
    install.std_deps('apt', ['python-pip', 'python3-pip', 'clang-format', 'cppcheck'], verbose, '\t')
    # PY2 Linter and YAPF
    install.std_deps('py2', ['pylint', 'yapf'], verbose, '\t')
    # PY3 Linter and YAPF --> To override pylint and yapf commands with py3 version
    install.std_deps('py3', ['pylint', 'yapf'], verbose, '\t')

    # Source `data/amz_source.sh` at the end of bashrc if it's not present
    l.chain("Appending `source ~/.amz/config/amz_source.sh` to bashrc", "\t", 0)

    try:
        BASHRC_LINE_EXISTS = "source ~/.amz/config/amz_source.sh\n" in open(f"{HOME_DIR}/.bashrc", 'r').readlines()

        if not BASHRC_LINE_EXISTS:
            with open(f"{HOME_DIR}/.bashrc", 'a') as f:
                f.write("\n# AMZ Tool Helper \nsource ~/.amz/config/amz_source.sh\n")
    except:
        l.end(1)

    # Setup bash autocomplete
    l.chain("Setting up bash autocompletion", "\t", 0)
    try:
        p = sp.run(f'activate-global-python-argcomplete --dest {AMZ_CONFIG_DIR}/',
                   shell=True,
                   stdout=sp.PIPE if not verbose else None,
                   stderr=sp.PIPE if not verbose else None)
        l.end(p.returncode)
    except:
        l.end(1)

    # Setting up auto-updater
    if not os.path.exists('/etc/systemd/system/amz_updater.timer'):
        l.chain("Setting up amz updater", "\t", 0)
        try:
            # Replace user var
            meta.substitute_in_file('__USER__', getpass.getuser(), f'{AMZ_DATA_DIR}/auto_update/amz_updater.service')
            # Copy files and reload systemd daemon
            p1 = sp.run(
                f'sudo cp {AMZ_DATA_DIR}/auto_update/amz_updater* /etc/systemd/system/ && sudo systemctl daemon-reload',
                shell=True,
                stdout=sp.PIPE if not verbose else None,
                stderr=sp.PIPE if not verbose else None)
            p2 = sp.run('sudo systemctl enable amz_updater.timer && sudo systemctl restart amz_updater.timer',
                        shell=True,
                        stdout=sp.PIPE if not verbose else None,
                        stderr=sp.PIPE if not verbose else None)
            l.end(p1.returncode + p2.returncode)
        except:
            l.end(1)

    # Termination point
    l.end(0)


# Repo Initialization
def amz_repo_init(verbose=False):
    sp_channel = None if verbose else sp.PIPE

    l = Loading("Initializing AMZ Repo")
    l.end(-2)

    l.chain("Preliminary Checks - are you inside the repo root? ", "\t")
    l.end(-3)

    # Check if `amz init gen` has been executed
    AMZ_INIT_EXECUTED = os.path.exists(f"{HOME_DIR}/.amz/config/amz_source.sh")
    if not AMZ_INIT_EXECUTED:
        print("Run `amz init gen` first!")
        l.end(1)
        return

    # Ask if user is in AMZ_ROOT
    while True:
        IN_AMZ_ROOT = input("\t\t (y/n): ").lower()
        if IN_AMZ_ROOT == 'n':
            print("Please run this command from the repo root")
            l.end(1)
            return
        if IN_AMZ_ROOT not in ['y', 'n']:
            print("Didn't quite catch you there!")
        else:
            break

    # Check if actually inside AMZ Repo
    if not os.path.exists('amz.yaml'):
        print("You are lying! Not in amz repo root")
        l.end(1)
        return

    # Fetch some data and write into amz-config YAML file
    l.chain("Configuring the repo", "\t", 0)

    # Set cur dir as AMZ Root and set git repo root
    amz_root_dir = os.getcwd()
    auto_repo = False
    try:
        git_config = RawConfigParser()
        git_config.read(f'{amz_root_dir}/.git/config')
        amz_git_remote = git_config.get('remote "origin"', 'url')
        if 'autonomous' in amz_git_remote and len(amz_git_remote.split('/')[1]) == 19:
            auto_repo = True
    except:
        print("Is it a git repo??? and has a valid remote?")
        l.end(1)
        return

    if auto_repo:
        try:
            amz_user_config = yaml.load(open(f'{AMZ_CONFIG_DIR}/amz-config.yaml'), Loader=yaml.FullLoader)
            amz_user_config['amz_repo_meta']['amz_root'] = amz_root_dir
            amz_user_config['amz_repo_meta']['amz_repo_git_src'] = amz_git_remote
            amz_user_config['amz_repo_meta']['amz_repo_config'] = f'{amz_root_dir}/amz.yaml'
            if amz_user_config['amz_tool_meta']['repos'][0] == '':
                amz_user_config['amz_tool_meta']['repos'][0] = amz_root_dir
            else:
                if amz_root_dir not in amz_user_config['amz_tool_meta']['repos']:
                    amz_user_config['amz_tool_meta']['repos'].append(amz_root_dir)
            with open(f'{AMZ_CONFIG_DIR}/amz-config.yaml', 'w') as f:
                yaml.dump(amz_user_config, f)
        except:
            print("Some issue with data files... Run `amz init gen` again. ")
            l.end(1)
            return

        # Update `amz_source.sh` with AMZ_ROOT
        meta.update_line_in_file('export AMZ_ROOT=', f"export AMZ_ROOT={amz_root_dir}",
                                 f"{AMZ_CONFIG_DIR}/amz_source.sh")

    if not auto_repo:
        try:
            amz_user_config = yaml.load(open(f'{AMZ_CONFIG_DIR}/amz-config.yaml'), Loader=yaml.FullLoader)
            if amz_user_config['amz_tool_meta']['repos'][0] == '':
                amz_user_config['amz_tool_meta']['repos'][0] = amz_root_dir
            else:
                if amz_root_dir not in amz_user_config['amz_tool_meta']['repos']:
                    amz_user_config['amz_tool_meta']['repos'].append(amz_root_dir)
            with open(f'{AMZ_CONFIG_DIR}/amz-config.yaml', 'w') as f:
                yaml.dump(amz_user_config, f)
        except:
            print("Some issue with data files... Run `amz init gen` again. ")
            l.end(1)
            return

    # Setup githooks
    l.chain("Installing githooks", "\t", 0)
    if verbose:
        l.end(-2)
    try:
        # Copy config files to root of repo: pre-commit, clang-format, yapf, cpplint, and pylint
        copy_tree(f'{AMZ_DATA_DIR}/githooks/config/', amz_root_dir)
        # Selectively append into .gitignore
        config_files = [file + '\n' for file in os.listdir(f'{AMZ_DATA_DIR}/githooks/config/')]
        gi_files = open('.gitignore').readlines()
        if not set(config_files).issubset(set(gi_files)):
            with open('.gitignore', 'a') as gi:
                add_files = [f for f in config_files if f not in gi_files]
                gi.writelines(['\n# Linter and Misc Configs\n'] + add_files + ['\n'])
        # Install pre-commit hook in hooks dir
        p = sp.run('pre-commit install --install-hooks --overwrite', shell=True, stdout=sp_channel, stderr=sp_channel)
        l.end(p.returncode)
    except:
        l.end(1)

    # Clone submodules
    if os.path.exists(f'{amz_root_dir}/.gitmodules'):
        l.chain("Cloning submodules", "\t", 0)
        if verbose:
            l.end(-2)
        try:
            os.chdir(amz_root_dir)
            p = sp.run('git submodule update --init --recursive', shell=True, stdout=sp_channel, stderr=sp_channel)
            l.end(p.returncode)
        except:
            l.end(1)

    # TODO: Clone bigfiles

    l.chain("Do you want to proceed with remaining setup? (Dependencies..)", "\t", 0)
    l.end(-3)
    INSTALL_DEPS = input('\t\t (y/n): ').lower()
    if INSTALL_DEPS == 'n':
        print("Exiting...")
        l.end(1)
        return
    if INSTALL_DEPS not in ['y', 'n']:
        print("Didn't understand! - Exiting...")
        l.end(1)
        return

    # Repo Deps Config
    amz_repo_config = yaml.load(open(f'{amz_root_dir}/amz.yaml'), Loader=yaml.FullLoader)

    # Install apt deps
    try:
        if amz_repo_config["apt-deps"] is not None:
            APT_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["apt-deps"]}'
            install.std_deps('apt', APT_DEPS_DIR, verbose, '\t')
    except (KeyError, TypeError):
        l.chain("No apt dependencies file found", "\t")
        l.end(1)

    # Install python2 deps
    try:
        if amz_repo_config["py2-deps"] is not None:
            PY2_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["py2-deps"]}'
            install.std_deps('py2', PY2_DEPS_DIR, verbose, '\t')
    except (KeyError, TypeError):
        l.chain("No Py2 dependencies file found", "\t")
        l.end(1)

    # Install python3 deps
    try:
        if amz_repo_config["py3-deps"] is not None:
            PY3_DEPS_DIR = f'{amz_root_dir}/{amz_repo_config["py3-deps"]}'
            install.std_deps('py3', PY3_DEPS_DIR, verbose, '\t')
    except (KeyError, TypeError):
        l.chain("No Py3 dependencies file found", "\t")
        l.end(1)

    return
