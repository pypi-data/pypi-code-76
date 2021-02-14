import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_visma_pay import __version__


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-visma-pay',
    version=__version__,
    description='Payment plugin for Visma Pay',
    long_description=long_description,
    url='https://gitlab.com/naaspeksi/pretix-visma-pay',
    author='Jaakko Rinta-Filppula',
    author_email='jaakko@r-f.fi',
    license='Apache',

    install_requires=[
        'requests>=2.24.0',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_visma_pay=pretix_visma_pay:PretixPluginMeta
""",
)
