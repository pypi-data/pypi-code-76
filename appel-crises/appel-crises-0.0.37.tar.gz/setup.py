#!/usr/bin/env python

import glob
import itertools
import os.path
import subprocess

from setuptools import setup
from setuptools.command import build_py


class FullBuild(build_py.build_py):
    def run(self):
        # Ensure the checked-out folder comes first.
        # We install the project as `pip install -e .`, but zest
        # will assemble the bdist_wheel from a temporary location;
        # this makes sure that the module picked as DJANGO_SETTINGS_MODULE
        # is the file from the temporary location, and all files get written
        # within that temporary location, and not the original git checkout.

        env = dict(os.environ)
        env['PYTHONPATH'] = ':'.join(
            [os.path.dirname(__file__)] + env.get('PYTHONPATH', '').split(':')
        )

        subprocess.check_call(['make', 'build'], env=env)
        return super().run()

    _expanded_package_data = False

    def _expand_package_data(self):
        if self._expanded_package_data:
            return

        def expand(package, pattern):
            for item in glob.iglob(os.path.join(package, pattern), recursive=True):
                yield item[len(package) + len(os.path.sep) :]

        self.package_data = {
            package: list(
                itertools.chain.from_iterable(
                    expand(package, pattern) for pattern in patterns
                )
            )
            for package, patterns in self.package_data.items()
        }
        self._expanded_package_data = True

    def find_data_files(self, package, src_dir):
        """Return filenames for package's data files in 'src_dir'"""
        self._expand_package_data()
        return super().find_data_files(package, src_dir)


setup(cmdclass={'build_py': FullBuild},)
