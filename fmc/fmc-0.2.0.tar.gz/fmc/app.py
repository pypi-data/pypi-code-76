#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from plumbum import cli, colors
from fmc.tasks import go, info, init, secure, git, cheatsheet
from fmc.utils.config_manager import ConfigManager
from fmc.utils.logger_formatter import setup_console_log_format

config_manager = ConfigManager()

class App(cli.Application):
    PROGNAME = colors.green
    VERSION = colors.green | "0.1.4"
    DESCRIPTION = colors.green | "A simple cli application For-My-Convenience."

    def main(self):
        if self.nested_command==None:
            self.help()


@App.subcommand("go")
class Go(cli.Application):
    """cd with alias"""

    eval = cli.Flag(["eval"], help="Output text for bash command eval")
    path = cli.SwitchAttr(["-s", "--set"], str, help="Set the path which current alias maps to.")
    
    def main(self, alias):
        task = go.GoTask(config_manager)

        if(self.path == None):
            task.go_alias(alias, self.eval)
        else:
            task.set_alias(alias, self.path)


@App.subcommand("secure")
class Secure(cli.Application):
    """Encryption/decryption with alias"""

    dry_run = cli.Flag(["dry-run"], help="Dry run.")
    path = cli.SwitchAttr(["-s", "--set"], str, help="Set the path which current alias maps to.")
    
    def main(self, alias):
        task = secure.SecureTask(config_manager)

        if self.path==None:
            task.secure_alias(alias, self.dry_run)
        else:
            task.set_alias(alias, self.path, self.dry_run)


@App.subcommand("init")
class Init(cli.Application):
    """Init something"""

    dry_run = cli.Flag(["dry-run"], help="Dry run.")

    def main(self):
        task = init.InitTask()
        task.run(self.dry_run)


@App.subcommand("info")
class Info(cli.Application):
    "Print environment info of fmc"
    
    def main(self):
        task = info.InfoTask(config_manager)
        task.print_env_info()


@App.subcommand("git")
class Git(cli.Application):
    "Shortcuts for git commands"
    
    def main(self):
        task = info.InfoTask(config_manager)
        task.print_env_info()


@Git.subcommand("init")
class GitInit(cli.Application):
    "Init git environment"
    
    def main(self):
        task = git.GitTask()
        task.init()


@App.subcommand("cheatsheet")
class CheatSheet(cli.Application):
    "Cheatsheet of commands"
    
    @cli.positional(str)
    def main(self, command = None):
        task = cheatsheet.CheatSheetTask(config_manager)
        if command == None:
            task.print_commands()
        else:
            task.run(command)


def main():
    setup_console_log_format()
    App.run()
    
if __name__=="fmc.app" or __name__=="__main__":
    main()