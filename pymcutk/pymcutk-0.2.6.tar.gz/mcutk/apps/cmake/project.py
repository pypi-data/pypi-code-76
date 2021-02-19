import os
import re
import glob
import platform

from mcutk.apps.projectbase import ProjectBase
from mcutk.exceptions import ProjectNotFound

def generate_build_cmdline(project, target, logfile):
    """Generate and return an executable commands."""

    osname = platform.system()
    if osname == "Windows":
        suffix = 'bat'
    else:
        suffix = 'sh'

    current_path = os.path.dirname(os.path.abspath(__file__))
    script_file = os.path.join(current_path, "cmake_build.{}".format(suffix)).replace('\\', '/')

    buildcmd = "{script} \"{prj_root}\" {target} \"{toolchain_file}\"".format(
        script=script_file,
        prj_root=project.prjdir,
        target=target,
        toolchain_file=project.toolchain_file,
    )

    if logfile:
        buildcmd = "{} >> {} 2>&1".format(buildcmd, logfile)

    return buildcmd


class Project(ProjectBase):
    """ Wraps a project defined in CMakeLists.txt."""

    PROJECT_EXTENSION = 'CMakeLists.txt'

    @classmethod
    def frompath(cls, path):
        """Return a project instance from a given file path or directory.

        If path is a directory, it will search the project file and return an instance.
        Else this will raise mcutk.apps.exceptions.ProjectNotFound.
        """

        if os.path.isfile(path) and path.endswith(cls.PROJECT_EXTENSION):
            return cls(path)

        if glob.glob(path + "/CMakeLists.txt") and glob.glob(path + "/build_all.*"):
            return cls(path + "/CMakeLists.txt")

        raise ProjectNotFound("Not found CMake project in path: %s"%path)

    def __init__(self, path, *args, **kwargs):
        super(Project, self).__init__(path, **kwargs)
        self._name = None
        self._targets = None
        self._toolchain_file = self.get_toolchain_file()
        self._conf = self._parse_project()

    def _parse_project(self):
        """Parse configurations from CMakeLists.txt.

        Returns:
            dict -- targets configuration
        """
        with open(self.prjpath, 'r') as fh:
            content = fh.read()

        # extract output name
        output_keywords = [
            r'add_library\([\w\-]+(\.)?\w+',
            r'add_executable\([\w\-]+(\.)?\w+',
            r'set_target_properties\(\w+(\.)?\w+',
            r'TARGET_LINK_LIBRARIES\(.*\.?\w+'
        ]

        excutable = None

        # since, release13, variable MCUX_SDK_PROJECT_NAME store the
        # executable configuration, example:
        # set(MCUX_SDK_PROJECT_NAME glow_cifar10.elf)
        match = re.compile("set\(MCUX_SDK_PROJECT_NAME (.*)\)").search(content)
        if match is not None:
            excutable = match.group(1)

        # compatible with old style
        if not excutable:
            for keyword in output_keywords:
                match = re.compile(keyword).search(content)
                if match != None:
                    excutable = match.group(0).split('(')[1].strip()
                    break

        # raise exception if there still not found
        if not excutable:
            raise ValueError("Unable to detect output definition in CMakeLists.txt. [%s]" % \
                             self.prjpath)

        self._appname = excutable.split('.')[0]

        if not self._targets:
            target_keyword = "CMAKE_C_FLAGS_"
            targets_list = re.findall(r"{}\w+ ".format(target_keyword), content)
            if not targets_list:
                target_keyword = "CMAKE_EXE_LINKER_FLAGS_"
                targets_list = re.findall(r"{}\w+ ".format(target_keyword), content)
            self._targets = [m.replace(target_keyword, '').lower().strip() for m in targets_list]

        # Add for vglite_acceptance, get extra path from EXECUTABLE_OUTPUT_PATH settings.
        extra_path = ""
        match = re.compile(r"SET\(EXECUTABLE_OUTPUT_PATH\s+\$\{ProjDirPath\}\/(.*)\/\$\{CMAKE_BUILD_TYPE\}\)", re.I).search(content)
        if match is not None:
            extra_path = match.group(1)

        # extract build types
        configs = dict()
        for tname in self._targets:
            if tname not in configs:
                if extra_path:
                    configs[tname] = "{}/{}/{}".format(extra_path, tname, excutable)
                else:
                    configs[tname] = "{}/{}".format(tname, excutable)
        return configs

    def get_toolchain_file(self):
        """This is a workaround to find the cmake toolchain file."""

        try:
            script_file = glob.glob(os.path.dirname(self.prjpath) + "/build_all.*")[0]
        except Exception:
            raise IOError("Unable to indentify CMAKE_TOOLCHAIN_FILE! "\
                          "Because script(build_all.sh/.bat) is not found!")

        with open(script_file, "r") as fobj:
            filecontent = fobj.read()

        toolchain_file = ''
        toolchain_ptn = re.compile(r'-DCMAKE_TOOLCHAIN_FILE="(\S+)" ')
        build_type_ptn = re.compile(r'-DCMAKE_BUILD_TYPE=(\S+) ')
        build_type_target_ptn = re.compile(r'build_(\w+)\.sh')

        match = toolchain_ptn.search(filecontent)
        if match:
            toolchain_file = match.group(1)

        # try to list configurations from shell script
        if not self._targets:
            self._targets = list(set(build_type_ptn.findall(filecontent)))
        
        # try to list configurations from shell script for vglite_acceptance
        if not self._targets:
            self._targets = list(set(build_type_target_ptn.findall(filecontent)))

        if toolchain_file:
            return toolchain_file

        # a work around to find toolchain file from parent folder
        # assum the toolchian is armgcc
        toolchain_file = _search_from_local(self.prjdir)
        if not toolchain_file:
            raise ValueError("not found toolchain file! project: %s" % self.prjpath)
        else:
            return toolchain_file

    @property
    def name(self):
        """Return application name"""
        return self._appname

    @property
    def toolchain_file(self):
        """Return a relative path for cmake_toolchain_file."""
        return self._toolchain_file

    @property
    def idename(self):
        """Return the toolchain name that the cmake defined."""
        if self.toolchain_file:
            filename = os.path.basename(self.toolchain_file)
            return filename.replace(".cmake", '').strip()
        return 'cmake'


def _search_from_local(path):
    current_dir = path
    while True:
        parent_dir = os.path.dirname(os.path.abspath(current_dir))
        # system root
        if parent_dir == current_dir:
            break
        _file = os.path.join(parent_dir, "tools/cmake_toolchain_files/armgcc.cmake")
        current_dir = parent_dir
        if os.path.exists(_file):
            return _file
    return ""
