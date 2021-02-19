import os
import re
import platform
import glob

from mcutk.apps.decorators import build
from mcutk.apps.idebase import IDEBase, Result, BuildResult
from mcutk.apps.eclipse import generate_build_cmdline


class APP(IDEBase):
    """Freescale Code Warrior"""

    OSLIST = ["Windows"]

    def __init__(self, *args, **kwargs):
        super(APP, self).__init__(*args, **kwargs)
        self.builder = os.path.join(self._path, "eclipse", "cwidec.exe")

    @build
    def build_project(self, project, target, logfile, **kwagrs):
        """Return a string about the build command line.

        Arguments:
            project {lpcx.Project} -- lpcx project object
            target {str} -- target name
            logfile {str} -- log file path
            workspace {str} -- default is ~/lpcx_mcutk

        Returns:
            string -- build commandline
        """
        workspace = kwagrs.get("workspace")
        buildcmd = generate_build_cmdline(
            '"%s"' % self.builder,
            workspace,
            project.prjdir,
            project.name,
            target)

        if logfile:
            buildcmd.append('>> "{}" 2>&1'.format(logfile))

        return " ".join(buildcmd)

    @property
    def is_ready(self):
        return os.path.exists(self.builder)

    @staticmethod
    def verify(path):
        """Verify installation."""
        return os.path.exists(path + "/eclipse/cwide.exe")

    @staticmethod
    def parse_build_result(exitcode, logfile):
        """Parse CW build result, exit code definitions:
            noerror warnnings: 0
            erros: none-zero

        Parser the log file by search the keyword:
            "Total number of warnings: <>".
        """
        result = Result.Errors
        if exitcode == 0 and logfile:
            result = Result.Passed
            with open(logfile, "r") as f:
                content = f.read()
                if re.search(r"Warning:", content):
                    result = Result.Warnings

        return BuildResult(result, None)

    @staticmethod
    def get_latest():
        """Find and return a installed instance from system."""

        path, version = get_latest()
        if path:
            return APP(path, version=version)
        else:
            return None

    @staticmethod
    def default_install_path(osname):
        default_path_table = {
            "Windows": r"C:\Freescale",
            "Linux": r"/usr/local"
        }
        return default_path_table[osname]


def get_latest():
    """Scan installed locations."""

    osname = platform.system()
    installations = []
    try:
        default_root_path = APP.default_install_path(osname)
        for per_folder in glob.glob(default_root_path + '/CW MCU**'):
            installations.append(os.path.join(default_root_path, per_folder))
    except IndexError:
        return None, None

    for install_path in installations:
        revfile = os.path.join(install_path, "eclipse/artifacts.xml")
        if os.path.exists(revfile):
            return install_path, "unknown"

    return None, None
