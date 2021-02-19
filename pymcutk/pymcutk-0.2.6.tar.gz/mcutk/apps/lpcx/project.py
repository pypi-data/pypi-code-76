import os
import glob
from mcutk.apps import eclipse
from mcutk.exceptions import ProjectNotFound

class Project(eclipse.Project):
    """LPCxpresso project parser."""

    @classmethod
    def frompath(cls, path):
        """Return a project instance from a given file path or directory.

        If path is a directory, it will search the project file and return an instance.
        Else this will raise mcutk.apps.exceptions.ProjectNotFound.
        """

        for filepath in glob.glob(path + "/.project"):
            filepath = os.path.abspath(filepath)
            if "lpcx" in filepath:
                drivers = filepath.replace("\\", "/").split("/")
                if "lpcx" in drivers:
                    return cls(filepath)

        raise ProjectNotFound("not found LPCX project")
