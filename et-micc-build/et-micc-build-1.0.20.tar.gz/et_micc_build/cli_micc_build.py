# -*- coding: utf-8 -*-
"""Command line interface build (no sub-commands)."""

import json
from pathlib import Path
import os
import platform
import shutil
import sys
import sysconfig
from types import SimpleNamespace

import click
import numpy.f2py

from et_micc.project import Project, micc_version
import et_micc.logger
import et_micc.utils


def get_extension_suffix():
    """Return the extension suffix, e.g. :file:`.cpython-37m-darwin.so`."""
    return sysconfig.get_config_var('EXT_SUFFIX')


def path_to_cmake_tools():
    """Return the path to the folder with the CMake tools."""
    p = (Path(__file__) / '..' / '..' / 'pybind11' / 'share' / 'cmake' / 'pybind11').resolve()
    return str(p)


def auto_build_binary_extension(package_path, module_to_build):
    """Set options for building binary extensions, and build
    binary extension *module_to_build* in *package_path*.

    :param Path package_path:
    :param str module_to_build:
    :return: exit_code
    """
    options = SimpleNamespace(
        package_path=package_path,
        module_name=module_to_build,
        build_options=SimpleNamespace(
            clean=False,
            save="",
            load="build_options",
            soft_link=True,
        ),
        verbosity=1,
    )
    for module_prefix in ["cpp", "f90"]:
        module_srcdir_path = package_path / f"{module_prefix}_{options.module_name}"
        if module_srcdir_path.exists():
            options.module_kind = module_prefix
            options.module_srcdir_path = module_srcdir_path
            options.build_options.build_tool_options = {}
            break
    else:
        raise ValueError(f"No binary extension source directory found for module '{module_to_build}'.")

    exit_code = build_binary_extension(options)

    msg = ("[ERROR]\n"
           "    Binary extension module 'bar{get_extension_suffix}' could not be build.\n"
           "    Any attempt to use it will raise exceptions.\n"
           ) if exit_code else ""
    return msg


def build_binary_extension(options):
    """Build a binary extension described by *options*.

    :param options:
    :return:
    """
    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = get_extension_suffix()

    build_options = options.build_options

    # Remove so file to avoid "RuntimeError: Symlink loop from ..."
    so_file = options.package_path / (options.module_name + extension_suffix)
    try:
        so_file.unlink()  # missing_ok=True only available from 3.8 on, not in 3.7
    except FileNotFoundError:
        pass

    build_log_file = options.module_srcdir_path / "micc-build.log"
    build_logger = et_micc.logger.create_logger(build_log_file, filemode='w')
    with et_micc.logger.log(build_logger.info, f"Building {options.module_kind} module '{options.module_name}':"):
        binary_extension = options.module_name + extension_suffix
        destination = (options.package_path / binary_extension).resolve()

        if options.module_kind in ('cpp', 'f90') and (options.module_srcdir_path / 'CMakeLists.txt').exists():
            output_dir = options.module_srcdir_path / '_cmake_build'
            build_dir = output_dir
            if build_options.clean:
                build_logger.info(f"--clean: shutil.removing('{output_dir}').")
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            with et_micc.utils.in_directory(output_dir):
                cmake_cmd = ['cmake',
                             '-D', f"PYTHON_EXECUTABLE={sys.executable}",
                             ]

                if options.module_kind == 'cpp':
                    cmake_cmd.extend(['-D', f"pybind11_DIR={path_to_cmake_tools()}"])

                for key, val in build_options.cmake.items():
                    cmake_cmd.extend(['-D', f"{key}={val}"])

                cmake_cmd.append('..')

                cmds = [
                    cmake_cmd,
                    ['make'],
                    ['make', 'install']
                ]
                exit_code = et_micc.utils.execute(
                    cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy()
                )
                if build_options.cleanup:
                    build_logger.info(f"--cleanup: shutil.removing('{build_dir}').")
                    shutil.rmtree(build_dir)
        else:
            raise RuntimeError("Bad module kind, or no CMakeLists.txt   ")

    return exit_code


def build_cmd(project):
    """
    Build binary extensions, i.e. f90 modules and cpp modules.

    :param str module_to_build: name of the only module to build (the prefix
        ``cpp_`` or ``f90_`` may be omitted). If not provided, all binrary
        extensions are built.
    :param types.SimpleNamespace options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are

        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **build_options**: all build options.
    """
    project_path = project.options.project_path
    if getattr(project, 'module', False):
        project.warning(
            f"Nothing to do. A module project ({project.project_name}) cannot have binary extension modules."
        )

    build_options = project.options.build_options

    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = get_extension_suffix()

    package_path = project.options.project_path / project.package_name
    dirs = os.listdir(package_path)
    succeeded = []
    failed = []
    for d in dirs:
        if ((package_path / d).is_dir()
                and (d.startswith("f90_") or d.startswith("cpp_"))
        ):
            if project.options.module_to_build and not d.endswith(project.options.module_to_build):
                # build only module module_to_build.
                continue

            module_kind, module_name = d.split('_', 1)
            binary_extension = package_path / (module_name + extension_suffix)
            project.options.module_srcdir_path = package_path / d
            project.options.module_kind = module_kind
            project.options.module_name = module_name
            project.options.package_path = package_path
            # project.options.build_options.build_tool_options = getattr(project.options.build_options, module_kind)
            project.exit_code = build_binary_extension(project.options)

            if project.exit_code:
                failed.append(binary_extension)
            else:
                succeeded.append(binary_extension)
    build_logger = project.logger
    if succeeded:
        build_logger.info("\n\nBinary extensions built successfully:")
        for binary_extension in succeeded:
            build_logger.info(f"  - {binary_extension}")
    if failed:
        build_logger.error("\nBinary extensions failing to build:")
        for binary_extension in failed:
            build_logger.error(f"  - {binary_extension}")
    if not succeeded and not failed:
        project.warning(
            f"No binary extensions found in package ({project.package_name})."
        )


@click.command()
@click.option('-v', '--verbosity', count=True
    , help="The verbosity of the program."
    , default=1
              )
@click.option('-p', '--project-path'
    , help="The path to the project directory. "
           "The default is the current working directory."
    , default='.'
    , type=Path
              )
@click.option('-m', '--module'
    , help="Build only this module. The module kind prefix (``cpp_`` "
           "for C++ modules, ``f90_`` for Fortran modules) may be omitted."
    , default=''
              )
@click.option('-b', '--build-type'
    , help="build type: any of the standard CMake build types: "
           "DEBUG, MINSIZEREL, RELEASE, RELWITHDEBINFO."
    , default='RELEASE'
              )
@click.option('--clean'
    , help="Perform a clean build."
    , default=False, is_flag=True
              )
@click.option('--cleanup'
    , help="Cleanup build directory after successful build."
    , default=False, is_flag=True
              )
@click.version_option(version=micc_version())
def main(verbosity
         , project_path
         , module
         , build_type
         , cleanup
         , clean
         ):
    """Build binary extension libraries (f90 and cpp modules)."""

    options = SimpleNamespace(
        verbosity=verbosity,
        project_path=project_path.resolve(),
        clear_log=False,
    )
    project = Project(options)

    with et_micc.logger.logtime(options):
        build_options = SimpleNamespace(cleanup=cleanup
                                        , clean=clean
                                        , cmake={'CMAKE_BUILD_TYPE': build_type}
                                        )

        project.options.module_to_build = module
        project.options.build_options = build_options

        build_cmd(project)

    sys.exit(project.exit_code)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
# eof
