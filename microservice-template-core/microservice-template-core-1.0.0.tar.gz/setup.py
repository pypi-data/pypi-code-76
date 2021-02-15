from setuptools import setup, find_packages
import os
import pwd
import grp
from setuptools import Command
SERVICE_NAME = 'microservice-template-core'
SERVICE_NAME_NORMALIZED = SERVICE_NAME.replace('-', '_')


def change_fcgi_permissions(files=None, folders=None):
    if files:
        for file in files:
            os.chmod(file, 0o755)
    if folders:
        for folder in folders:
            os.chmod(folder, 0o655)


def create_folders():
    directories = [f'/opt/{SERVICE_NAME_NORMALIZED}', f'/var/log/{SERVICE_NAME_NORMALIZED}']
    uid = pwd.getpwnam("root").pw_uid
    gid = grp.getgrnam("root").gr_gid
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.chown(directory, uid, gid)


class CustomInstallCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        create_folders()
        change_fcgi_permissions([],
                                [f'/opt/fcgi/'])


class Tests(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        print("Test passed.")


tests_require = [],

setup(
    name=SERVICE_NAME,
    version='1.0.0',
    description="Microservice template core",
    url='',
    include_package_data=True,
    author='',
    author_email='',
    classifiers=[
    ],
    keywords=[],
    packages=find_packages(),
    install_requires=[
        'Flask',
        'APScheduler',
        'flask_cors',
        'flask_restplus',
        'Werkzeug==0.16.1',
        'python-logging-loki',
        'prometheus_client',
        'prometheus_flask_exporter',
        'flask_sqlalchemy',
        'opentelemetry-api',
        'opentelemetry-sdk',
        'opentelemetry-exporter-jaeger',
        'flask_jwt_extended==3.16.0'
    ],
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            f'{SERVICE_NAME} = {SERVICE_NAME_NORMALIZED}.core:main',
        ]
    },
    zip_safe=False,
    cmdclass={
        'configure': CustomInstallCommand,

    },
    data_files=[]
)


