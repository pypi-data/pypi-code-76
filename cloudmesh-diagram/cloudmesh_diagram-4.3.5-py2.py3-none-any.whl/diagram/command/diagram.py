from cloudmesh.diagram.diagram import Diagram

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
                diagram set CLUSTER --hostname=NAMES
                diagram set CLUSTER NAME ATTRIBUTE VALUE
                diagram rack CLUSTER
                diagram net CLUSTER


          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

          Example:

                Installation:
                    pip install cloudmesh-diagram

                Create a rack diagram:
                    cms diagram set d --hostname="red[00-04]"
                    cms diagram set d red01 rack.color blue
                    cms diagram set d red02 net.color red
                    cms diagram rack d
                    cms diagram net d


        """

        map_parameters(arguments, 'hostname')

        if arguments.set and arguments.hostname:

            hostnames = Parameter.expand(arguments.hostname)
            rack = Diagram(hostnames)
            name = arguments.CLUSTER
            rack.save(name)

        elif arguments.set and arguments.NAME:
            rack = Diagram()
            rack.load(arguments.CLUSTER)
            data = {
                arguments.ATTRIBUTE: arguments.VALUE
            }
            rack.set(arguments.NAME, **data)
            rack.save(arguments.CLUSTER)

        elif arguments.rack:
            svg = f"{arguments.CLUSTER}-rack"
            rack = Diagram()
            rack.load(arguments.CLUSTER)
            rack.render(kind="rack")
            rack.save_diagram(svg)
            rack.svg(svg, kind="rack")
            rack.view(svg)

        elif arguments.net:

            svg = f"{arguments.CLUSTER}-net"

            net = Diagram()
            net.load(arguments.CLUSTER)
            net.render(kind="bridge")
            net.save_diagram(svg)
            net.svg(svg, kind="net")
            net.view(svg)

        return ""
