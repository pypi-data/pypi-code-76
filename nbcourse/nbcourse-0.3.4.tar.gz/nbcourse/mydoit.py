"""Define some Doit customizations"""

from doit.cmd_help import Help
from doit.doit_cmd import DoitMain
from doit.cmd_base import NamespaceTaskLoader
import inspect


class MyDoitMain(DoitMain):
    BIN_NAME = globals()['__package__']


class MyHelp(Help):
    """Extend doit Help class to add a get_usage() function"""

    @staticmethod
    def get_usage(cmds):
        """return doit "usage" (basic help) instructions"""
        msg = "\n"
        for cmd_name in sorted(cmds.keys()):
            cmd = cmds[cmd_name]
            msg += "  {:16s}      {}\n".format(cmd_name, cmd.doc_purpose)
        msg += "\n"
        for line in [
                "  {}                  show doit's help\n",
                "  {} task             show help on task dictionary fields\n",
                "  {} <command>        show command usage\n",
                "  {} <task-name>      show task usage\n"]:
            msg += line.format("help")
        return msg


class MyDoitHelp(DoitMain):
    """Extend DoitMain class to add a get_help() function"""

    def get_help(self):
        """return help usage as string"""

        # get list of available commands
        sub_cmds = self.get_cmds()
        doit_help = MyHelp(task_loader=self.task_loader,
                           config=self.config,
                           bin_name='',
                           cmds=sub_cmds)
        return doit_help.get_usage(sub_cmds.to_dict())


class ClassTaskLoader(NamespaceTaskLoader):
    """Implementation of a loader of tasks from a Class namespace"""

    def __init__(self, classname):
        super().__init__()
        self.namespace = dict(inspect.getmembers(classname))
