import os
import re
import glob
import logging
import platform
import subprocess

from distutils.version import LooseVersion
from mcutk.apps.decorators import build
from mcutk.apps.idebase import IDEBase, BuildResult
from mcutk.elftool import transform_elf_basic
from mcutk.apps.cmake import generate_build_cmdline


class APP(IDEBase):
    """GNU ARM GCC compiler.

    CMake and ARM-GCC build explanation:
        - Generate Makefile:
        >>> cmake -DCMAKE_TOOLCHAIN_FILE={path}/armgcc.cmake -G "{MinGW|Unix} Makefiles" -DCMAKE_BUILD_TYPE=debug

        - Start build with make tool or mingw32-make:
        >>> make -C "<path-to-makefile-directory>" -j4
        >>> mingw32-make -C "<path-to-makefile-directory>" -j4

        - Compile. Armgcc compiler will be called to compile in makefile.

    CMake is a cross-platform build system generator. Projects specify their build
    process with platform-independent CMake listfiles included in each directory
    of a source tree with the name CMakeLists.txt. Users build a project by using
    CMake to generate a build system for a native tool on their platform.

    GNU Make is a tool which controls the generation of executables and other non-source
    files of a program from the program's source files. Make gets its knowledge of how to
    build your program from a file called the makefile, which lists each of the non-source
    files and how to compute it from other files. When you write a program, you should
    write a makefile for it, so that it is possible to use Make to build and install the
    program.


    """

    OSLIST = ["Windows", "Linux", "Darwin"]


    @property
    def is_ready(self):
        return os.path.exists(self.path)

    @build
    def build_project(self, project, target, logfile, **kwargs):
        """Return a command line string for armgcc. The build commands
        are packaging into a shell/bat script.

        Arguments:
            project {armgcc.Project} -- armgcc project object
            target {string} -- target name
            logfile {string} -- log file path

        Returns:
            string -- commandline string.
        """
        os.environ["ARMGCC_DIR"] = self.path
        return generate_build_cmdline(project, target, logfile)

    def transform_elf(self, type, in_file, out_file):
        """Convert ELF to specific type.
        Called <mcutk>/bin/arm-none-eabi-objcopy to do the job.

        Supported types: bin, ihex, srec.

        Arguments:
            in_file {str} -- path to elf file.
            out_file {str} -- output file
            type {str} -- which type you want to convert.

        Raises:
            ReadElfError -- Unknown elf format will raise such error
            Exception -- Convert failed will raise exception

        Returns:
            bool
        """
        executor = os.path.join(self.path, 'bin/arm-none-eabi-objcopy')
        if os.name == 'nt':
            executor += '.exe'

        return transform_elf_basic(type, in_file, out_file, executor)

    @staticmethod
    def verify(path):
        '''
        verify the path of compiler is avaliable
        '''
        return os.path.exists(path)

    @staticmethod
    def get_latest():
        """Search and return a latest armgcc instance from system.

        Returns:
            <armgcc.APP object> or None
        """
        path, version = find_armgcc_latest()
        if path:
            return APP(path, version=version)
        else:
            return None

    @staticmethod
    def parse_build_result(exitcode, logfile):
        """GNU make exits with a status of zero if all makefiles were successfully
        parsed and no targets that were built failed. A status of one will be
        returned if the -q flag was used and  make  determines  that a target
        needs to be rebuilt. A status of two will be returned if any errors
        were encountered.
        """

        if exitcode != 0:
            return BuildResult.map("error")

        if not logfile:
            return BuildResult.map("pass")

        p = re.compile(r'warning:')

        with open(logfile) as fobj:
            for line in fobj:
                if p.search(line) != None:
                    return BuildResult.map("warning")

        return BuildResult.map("pass")



def find_armgcc_latest():
    """Get the latest armgcc version

    Returns:
        tuple -- (path, version)
    """

    default_path_table = {
        "Windows": [
            "C:/Program Files (x86)/GNU Arm Embedded Toolchain",
            "C:/Program Files (x86)/GNU Tools ARM Embedded"
            ],
        "Linux": ["/usr/local"],
        "Darwin": ["/usr/local"],
    }

    search_paths = default_path_table.get(platform.system())
    return _find_armgcc_latest_version(search_paths)


def _find_armgcc_latest_version(search_paths):
    osname = platform.system()
    versions_dict = {}

    for root_path in search_paths:
        if not os.path.exists(root_path):
            continue

        # build the glob serach pattern
        if osname == "Windows":
            gcc_exes = glob.glob(root_path + "/*/bin/arm-none-eabi-gcc.exe")
        else:
            gcc_exes = glob.glob(root_path + "/gcc-arm-none-eabi*/bin/arm-none-eabi-gcc")

        for gcc_exe in gcc_exes:
            instance_path = os.path.abspath(os.path.join(gcc_exe, "../../"))
            if osname == "Windows":
                version = os.path.basename(instance_path).replace(" ", "-").strip()
            else:
                version = os.path.basename(instance_path).replace("gcc-arm-none-eabi-", "")

            # Try to get version from: arm-none-eabi-gcc --version
            if not version:
                version_content = os.popen("\"{}\" --version".format(gcc_exe)).read()
                ret = re.search(r"\d\.\d\.\d", version_content)
                if ret is not None:
                    version = ret.group()

            if version:
                versions_dict[version] = instance_path

    if not versions_dict:
        return None, None

    latest_v = sorted(versions_dict.keys(), key=lambda v: LooseVersion(v))[-1]
    return versions_dict[latest_v], latest_v

