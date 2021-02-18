from .magic import line_magic, arg
from iot_device import Config
from iot_device import cd

from subprocess import run, PIPE
from glob import glob
import os, shlex, shutil


@arg('-p', '--projects', nargs='*', default=None, help="host projects, defaults to specifiation in hosts.py")
@arg('-i', '--implementation', default=None, help="sys.implementation.name of current device")
@arg('-c', '--compiler', default=None, help="Path to the compiler, defaults to `$IOT49/bin/{implementation}/mpy-cross`")
@arg('-a', '--args', default="", help="Arguments passed to `mpy-cross`")
@line_magic
def mpycross_magic(kernel, args):
    """Compile .py files in projects folders.

Compiles files in each `project` folder to a new folder `.project-{implementation}`.

Examples:

    %mpycross
    %mpycross --projects base my-great-project
    %mpycross --compiler /usr/local/mpy-cross --args="-O2 -mno-unicode"
"""
    projects = args.projects
    if not projects: projects = kernel.device.projects
    implementation = args.implementation
    if not implementation:
        with kernel.device as repl:
            implementation = repl.implementation
    compiler = args.compiler
    if not compiler: compiler = os.path.join(Config.iot49_dir(), 'bin', implementation, 'mpy-cross')
    compiler_args = args.args

    n = 0
    for project in projects:
        with cd(os.path.join(Config.iot49_dir(), project)):
            for src in glob('./**/*.py', recursive=True):
                dst = os.path.join(Config.iot49_dir(), f'.{project}-{implementation}', src.replace('.py', '.mpy'))
                if not os.path.isfile(dst) or (os.path.getmtime(src) > os.path.getmtime(dst)):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    kernel.print(f"compiling   {os.path.normpath(os.path.join(project, src))}")
                    cmd = f"{compiler} {compiler_args} -s {os.path.basename(src)} -o {dst} {src}"
                    try:
                        result = run(shlex.split(cmd), stdout=PIPE)
                        kernel.print(result.stdout.decode('utf-8'))
                    except FileNotFoundError as e:
                        kernel.stop(e)
                    n += 1

    if n == 0:
        kernel.print("all mpy files are up-to-date")
