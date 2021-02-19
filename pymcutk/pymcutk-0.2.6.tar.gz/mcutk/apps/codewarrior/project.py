import os
import glob
from mcutk.exceptions import ProjectNotFound
from mcutk.apps import eclipse

class Project(eclipse.Project):
    """Code Warrior project object

    This class could parser the settings in .cproject and .project.
    Parameters:
        prjpath: path of .project
    """

    @classmethod
    def frompath(cls, path):

        if os.path.isfile(path):
            return cls(path)

        for filepath in glob.glob(path + "/.project"):
            parts = os.path.abspath(filepath).replace("\\", "/").split("/")
            if "codewarrior" in parts or "cw" in parts:
                return cls(filepath)

        raise ProjectNotFound("not found Code Warrior project")
