"""
vmon - vmon-cli

09-12-2020


codenio - Aananth K
aananthraj1995@gmail.com
"""

import click
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.startswith('__'):
                continue
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']


cli = MyCLI(help='vmon - I-Mon Spectrum Viewer and Exporter')

if __name__ == '__main__':
    cli()
