import textwrap
from cloudmesh.common.util import path_expand
import oyaml as yaml
import subprocess

class Network:

    def __init__(self, hostnames=None):
        pass
        self.hostnames = hostnames

    def diagram(self):

        header = textwrap.dedent("""
        nwdiag {
          # network internet{
          #    address = "xxx.xxx.xxx.xxx"
          #    modem
          #}
          network wifi {
              address = "192.168.50.x"
              # modem
          
              red [address = "192.168.50.100"];
              laptop [address = "192.168.50.100"];
              }
          network internal {
              address = "10.0.0.x";
        """)

        servers = []

        counter = 2
        for name in self.hostnames[1:]:
            server = f'      {name} [address = "10.0.0.{counter}"];'
            servers.append(server)
            counter = counter + 1

        name = self.hostnames[0]
        counter = 1
        server = f'      {name} [address = "10.0.0.{counter}"];'
        servers.append(server)

        servers = "\n".join(servers)

        footer = textwrap.dedent("""
          }
        }
        """)

        self.diag = header + servers + footer
        return self.diag

    def svg(self, name):
        filename = path_expand(name)

        c = self.diagram()

        with open(f"{filename}.diag", 'w') as f:
            f.write(self.diag)
            f.flush()

        cmd = ['nwdiag', "-T", "svg", f"{filename}.diag"]
        subprocess.Popen(cmd).wait()

    def view(self, name):
        filename = path_expand(name)
        cmd = ['open', f"{filename}.svg"]
        subprocess.Popen(cmd)

