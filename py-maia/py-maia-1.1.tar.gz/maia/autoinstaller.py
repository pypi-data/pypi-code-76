import traceback
import sys
import os


def clear():
    if sys.platform in ('linux', 'linux2'):
        os.system('clear')
    elif sys.platform == 'win32':
        os.system('cls')
        print('\n')


def is_module(trace):
    if 'ModuleNotFoundError' in trace:
        module = trace.split("'")[1] if "'" in trace else None
        return module
    return None


def write_startfile(trace):
    with open('start_file.txt', 'w') as stfile:
        stfile.write(trace)
        stfile.close()


class InstallModuleError(Exception):
    """Static error class"""
    def __init__(self, message):
        super().__init__(message)


class AutoInstaller:
    def __init__(self):
        self.trace = traceback.format_exc()
        self.install()
        self.restart()

    def install(self):
        trace = self.trace
        if trace is not None:
            if is_module(trace):
                if os.path.exists('start_file.txt'):
                    last_traceback = open('start_file.txt', 'r').read()
                    if last_traceback == trace:
                        raise InstallModuleError(f"Can't install module named '{is_module(trace)}'")
                os.system(f"pip install {is_module(trace)}")
                write_startfile(trace)
                clear()

    def restart(self):
        trace = self.trace
        split = trace.split('\n')
        file = [i.split('"')[1] for i in split if 'File "' in i][0]
        os.system(f"python {file}")
        sys.exit()
