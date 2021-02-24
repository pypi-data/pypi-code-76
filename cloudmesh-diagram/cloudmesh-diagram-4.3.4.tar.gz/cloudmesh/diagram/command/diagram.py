from cloudmesh.diagram.rack import Rack
from cloudmesh.diagram.network import Network

from cloudmesh.common.parameter import Parameter
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.command import map_parameters


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
                diagram net RACK --hostname=NAMES


          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

          Example:

                Installation:
                    pip install cloudmesh-diagram

                Create a rack diagram:
                    cms diagram rack d --hostname="red[00-04]"
                    cms diagram rack d red01 color blue
                    cms diagram view d

                Create a network diagram:
                    cms diagram net  n --hostname="red,red[01-04]"

                    The network diagram does not yet have the ability to set
                    attributes


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
            data = {
                arguments.ATTRIBUTE: arguments.VALUE
            }
            rack.set(arguments.NAME, **data)
            rack.save(arguments.RACK)

        elif arguments.net:

            hostnames = Parameter.expand(arguments.hostname)

            net = Network(hostnames=hostnames)

            net.svg(arguments.RACK)
            net.view(arguments.RACK)


        return ""
