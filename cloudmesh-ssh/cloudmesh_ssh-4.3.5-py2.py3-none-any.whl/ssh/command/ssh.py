import os

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.ssh.ssh_config import ssh_config
from cloudmesh.common.util import path_expand
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command


class SshCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_ssh(self, args, arguments):
        """
        ::

            Usage:
                ssh config list [--output=OUTPUT]
                ssh config add NAME IP [USER] [KEY]
                ssh config delete NAME

            Arguments:
              NAME        Name or ip of the machine to log in
              list        Lists the machines that are registered and
                          the commands to login to them
              PARAMETERS  Register te resource and add the given
                          parameters to the ssh config file.  if the
                          resource exists, it will be overwritten. The
                          information will be written in /.ssh/config
              USER        The username for the ssh resource
              KEY         The location of the public keye used for
                          authentication to the host

            Options:
               --output=OUTPUT   the format in which this list is given
                                 formats includes cat, table, json, yaml,
                                 dict. If cat is used, it is just printed as
                                 is. [default: table]

            Description:
                ssh config list
                    lists the hostsnames that are present in the ~/.ssh/config file

                ssh config add NAME IP [USER] [KEY]
                    registers a host i ~/.ssh/config file
                    Parameters are attribute=value pairs

                ssh config delete NAME
                    deletes the named host from the ssh config file

            Examples:

                 ssh config add blue 192.168.1.245 gregor

                     Adds the following to the !/.ssh/config file

                     Host blue
                          HostName 192.168.1.245
                          User gergor
                          IdentityFile ~/.ssh/id_rsa.pub

        """

        map_parameters(arguments, "output")

        if arguments.config and arguments.list:
            # ssh config list [--output=OUTPUT]"

            hosts = dict(ssh_config().hosts)

            # Make keywords uniform
            for host in hosts:

                if "HostName" in hosts[host]:
                    hosts[host]["Hostname"] = hosts[host]["HostName"]
                    del hosts[host]["HostName"]
                if "Identityfile" in hosts[host]:
                    hosts[host]["IdentityFile"] = hosts[host]["Identityfile"]
                    del hosts[host]["Identityfile"]

            print(Printer.write(hosts,
                                order=['host', 'Hostname', 'User', 'IdentityFile']))

        elif arguments.config and arguments.add:
            # ssh config add NAME IP [USER] [KEY]

            variables = Variables()

            user = Parameter.find("user",
                                  arguments,
                                  variables.dict())

            key = Parameter.find("key",
                                 arguments,
                                 variables.dict(),
                                 {"key": "~/.ssh/id_rsa.pub"})

            name = arguments.NAME or variables['vm']

            ip = arguments.IP

            hosts = ssh_config()

            if name in hosts.hosts:
                Console.error("Host already in ~/.ssh/config")
                return ""

            hosts.generate(host=name, hostname=ip, identity=key, user=user)

        elif arguments.config and arguments.add:
            # ssh host add NAME

            location = path_expand("~/.ssh/known_hosts")
            name = arguments.NAME
            os.system("ssh-keygen -R {name}")
            os.system(f"ssh-keyscan -H {name} >> {location}")

        elif arguments.config and arguments.delete:
            # ssh host delete NAME

            name = arguments.NAME
            try:
                os.system("ssh-keygen -R {name}")
            except:
                pass
            ssh_config.delete(name)


