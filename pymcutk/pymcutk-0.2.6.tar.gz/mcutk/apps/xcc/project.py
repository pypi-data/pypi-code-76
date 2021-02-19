import re
from mcutk.apps import cmake
from mcutk.exceptions import ProjectNotFound

class Project(cmake.Project):
    """xcc project object

    This class could parser the settings in CMakeLists.txt & build_all.sh.
    Parameters:
        prjpath: path of CMakeLists.txt

    """
    @classmethod
    def frompath(cls, path):
        instance = super(Project, cls).frompath(path)
        if instance and instance.idename != "xcc":
            raise ProjectNotFound("This is not xcc CMakeLists.txt")
        return instance

    def get_xtensa_core(self):
        """Find xtensa-core in CMakeLists.txt."""
        with open(self.prjpath, 'r') as fobj:
            content = fobj.read()

        core_name = None
        pattern = r"--xtensa-core=(\w+)"
        ret = re.search(pattern, content)
        if ret:
            core_name = ret.group(1).strip()

        return core_name
