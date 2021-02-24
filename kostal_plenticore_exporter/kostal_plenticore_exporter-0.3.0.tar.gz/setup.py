# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kostal_plenticore_exporter']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0', 'kostalplenticore>=0.3,<0.4', 'prometheus-client>=0.7']

entry_points = \
{'console_scripts': ['kostal-plenticore-exporter = '
                     'kostal_plenticore_exporter.cli:cli']}

setup_kwargs = {
    'name': 'kostal-plenticore-exporter',
    'version': '0.3.0',
    'description': 'A Prometheus exporter for the Kostal Plenticore series of inverters.',
    'long_description': '=====================================\nKostal Plenticore Prometheus Exporter\n=====================================\n\nThis is a Prometheus exporter for the `Kostal Plenticore <https://www.kostal-solar-electric.com/en-gb/products>`_ series of inverters.\nIt exports the metrics exposed by the inverter in `Prometheus <https://prometheus.io>`_ format.\nThis way it can be ingested into Prometheus and used for `Grafana <https://grafana.com/>`_ dashboards or to trigger notifications in case of failure events.\n\nUsage\n=====\n\nRun the ``kostal-plenticore-exporter`` passing it the IP address of the inverter and the password of the operator user.\nAs command line arguments can be seen by other users on the system, the password should be passed via environment\nvariable::\n\n    PASSWORD="my super secret" kostal-plenticore-exporter 192.168.1.3\n\nThe metrics will be default be exposed at `<http://localhost:9876/>`_.\nSee ``kostal-plenticore-exporter --help`` for all metrics available.\n\nAlternatively, you can also invoke the Python module: ``python3 -m kostal_plenticore_exporter --help``.\n\nLicense\n=======\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see `<http://www.gnu.org/licenses/>`_.\n',
    'author': 'Matthias Bach',
    'author_email': 'marix@marix.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/Marix/kostal-plenticore-exporter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
