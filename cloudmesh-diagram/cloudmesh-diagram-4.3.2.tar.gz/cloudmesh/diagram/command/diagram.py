from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter
from cloudmesh.shell.command import map_parameters
from cloudmesh.diagram.rack import Rack

class DiagramCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_diagram(self, args, arguments):
        """
        ::

          Usage:
                diagram rack RACK --hostname=NAMES
                diagram rack RACK NAME ATTRIBUTE VALUE
                diagram rack RACK
                diagram view RACK


          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

          Example:

                Installation:
                    pip install cloudmesh-diagram

                Uassage:
                    cms diagram rack d --hostname="red[00-04]"
                    cms diagram rack d red01 color blue
                    cms diagram view d


        """

        map_parameters(arguments, 'hostname')

        if arguments.rack and arguments.hostname:

            hostnames = Parameter.expand(arguments.hostname)
            rack = Rack(hostnames)
            name = arguments.RACK
            rack.save(name)

        elif arguments.view:
            rack = Rack()
            rack.load(arguments.RACK)
            rack.render()
            rack.svg(arguments.RACK)
            rack.view(arguments.RACK)

        elif arguments.rack:
            rack = Rack()
            rack.load(arguments.RACK)
            data = {arguments.ATTRIBUTE: arguments.VALUE }
            rack.set(arguments.NAME, **data)
            rack.save(arguments.RACK)

        return ""
