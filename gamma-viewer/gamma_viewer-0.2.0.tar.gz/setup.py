"""Setup Jupyter notebook react extension."""
from __future__ import print_function
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import os
import sys
import platform
from distutils import log

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, 'js')
is_repo = os.path.exists(os.path.join(here, '.git'))

npm_path = os.pathsep.join([
    os.path.join(node_root, 'node_modules', '.bin'),
    os.environ.get('PATH', os.defpath),
])

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = """
# Gamma Viewer
----
Jupyter Notebook javascript extension for viewing Translator Standard messages in an analytic UI.
----
## Installation
```bash
    pip install gamma_viewer
    jupyter nbextension enable --py gamma_viewer
```
## Usage
```python
    from gamma_viewer import GammaViewer
    from IPython.display import display
    import json

    with open('translator_standard_message.json', 'r') as f:
        res = json.load(f)

    view = GammaViewer(props={"data":res})
    display(view)
```
"""


def js_prerelease(command, strict=False):
    """Decorator for building minified js/css prior to another command."""
    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj('jsdeps')
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command('jsdeps')
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn('rebuilding js and css failed')
                    if missing:
                        log.error('missing files: %s' % missing)
                    raise e
                else:
                    log.warn('rebuilding js and css failed (not a problem)')
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)
    return DecoratedCommand


def update_package_data(distribution):
    """Update package_data to catch changes during setup."""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


class NPM(Command):
    description = 'install package.json dependencies using npm'

    user_options = []

    node_modules = os.path.join(node_root, 'node_modules')

    targets = [
        os.path.join(here, 'gamma_viewer', 'static', 'extension.js')
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            # shell=True needs to be passed for windows to look at non .exe files.
            shell = (sys.platform == 'win32')
            check_call(['npm', '--version'], shell=shell)
            return True
        except:
            return False

    def should_run_npm_install(self):
        package_json = os.path.join(node_root, 'package.json')
        node_modules_exists = os.path.exists(self.node_modules)
        return self.has_npm()

    def run(self):
        has_npm = self.has_npm()
        if not has_npm:
            log.error("`npm` unavailable.  If you're running this command using sudo, make sure `npm` is available to sudo")

        env = os.environ.copy()
        env['PATH'] = npm_path
        shell = (sys.platform == 'win32')

        if self.should_run_npm_install():
            log.info("Installing build dependencies with npm.  This may take a while...")
            # shell=True needs to be passed for windows to look at non .exe files.
            check_call(['npm', 'install'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr, shell=shell)
            os.utime(self.node_modules, None)

        # build production javascript
        check_call(['npm', 'run', 'build'], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr, shell=shell)

        for t in self.targets:
            if not os.path.exists(t):
                msg = 'Missing file: %s' % t
                if not has_npm:
                    msg += '\nnpm is required to build a development version of Gamma Viewer'
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)


setup_args = {
    'name': 'gamma_viewer',
    'version': '0.2.0',
    'description': 'Interactive Translator UI for the Jupyter notebook, using React.',
    'long_description': LONG_DESCRIPTION,
    'long_description_content_type': 'text/markdown',
    'license': 'MIT',
    'include_package_data': True,
    'data_files': [
        ('share/jupyter/nbextensions/gamma_viewer', [
            'gamma_viewer/static/extension.js'
        ]),
        ('etc/jupyter/nbconfig/notebook.d', ['gamma_viewer.json'])
    ],
    'install_requires': [
        'jupyter-react~=0.1.3'
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
        'build_py': js_prerelease(build_py),
        'egg_info': js_prerelease(egg_info),
        'sdist': js_prerelease(sdist, strict=True),
        'jsdeps': NPM,
    },
    'author': 'CoVar Applied Technologies',
    'url': 'https://github.com/ranking-agent/gamma-viewer',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
        'Translator',
        'plotting',
        'react',
    ],
    'classifiers': [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
    ],
}

setup(**setup_args)
