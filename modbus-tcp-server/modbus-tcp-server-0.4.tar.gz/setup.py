from setuptools import find_packages
from distutils.core import setup
from modbus_tcp_server import __version__


setup(version=__version__,
      packages=find_packages(include=['modbus_tcp_server', 'modbus_tcp_server.*']),
      install_requires=['satella'],
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
      zip_safe=True,
      entry_points={
            'console_scripts': [
                  'modbus-tcp-server = modbus_tcp_server.run:run'
            ]
      }

      )
