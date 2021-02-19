from mcutk.apps import cmake
from mcutk.exceptions import ProjectNotFound

class Project(cmake.Project):
    """
    ARMGCC project object

    This class could parser the settings in CMakeLists.txt & build_all.sh.
    Parameters:
        prjpath: path of CMakeLists.txt

    """

    @classmethod
    def frompath(cls, path):
        instance = super(Project, cls).frompath(path)
        if instance and instance.idename != "armgcc":
            raise ProjectNotFound("This is not armgcc CMakeLists.txt")
        return instance
