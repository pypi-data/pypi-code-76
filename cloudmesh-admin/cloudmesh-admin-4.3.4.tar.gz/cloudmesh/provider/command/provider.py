import json
import textwrap

from cloudmesh.common.Tabulate import Printer
from cloudmesh.common.console import Console
from cloudmesh.provider.find import find
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters


class ProviderCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/main/cloudmesh_client/shell/plugins/KeyCommand.py
    # see https://github.com/cloudmesh/client/blob/main/cloudmesh_client/shell/plugins/AkeyCommand.py

    # noinspection PyUnusedLocal
    @command
    def do_provider(self, args, arguments):
        """
        ::

           Usage:
             provider list [--output=OUTPUT]
             provider info SERVICE NAME WHAT

           Arguments:
             NAME           The name of the key.

           Options:
              --output=OUTPUT               the format of the output [default: table]


           Description:

                What: output, sample

           Examples:
             Getting the sample and output from provides via a command

               cms provider info compute openstack sample
               cms provider info compute openstack output
               cms provider list --output=json
               cms provider list

q        """

        map_parameters(arguments, 'output')

        if arguments.info:
            try:
                service = arguments.SERVICE
                name = arguments.NAME
                what = arguments.WHAT

                services = find()

                for provider in services:

                    try:

                        if provider['service'] == service and provider['name'] == name:

                            if arguments.WHAT == 'sample':
                                print(textwrap.dedent(
                                    provider["provider"].sample))
                            elif arguments.WHAT == 'output':
                                print(json.dumps(provider["provider"].output, indent=4))
                                print()

                    except Exception as e:
                        print(e)

            except:
                Console.error("Problem getting the Provider info")
                return ""

        elif arguments.list:

            print(arguments.output)
            _paths = find()

            for entry in _paths:
                del entry["provider"]  # can not be printed
            print(
                Printer.write(_paths,
                              order=["service", "name", "active", "path"],
                              output=arguments.output)
            )

        return ""
