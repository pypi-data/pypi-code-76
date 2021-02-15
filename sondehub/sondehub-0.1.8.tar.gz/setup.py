# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sondehub']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.44,<2.0.0', 'paho-mqtt>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['sondehub = sondehub:__main__.main']}

setup_kwargs = {
    'name': 'sondehub',
    'version': '0.1.8',
    'description': 'SDK to access SondeHub open data',
    'long_description': 'Simple realtime streaming SDK for sondehub.org V2 API.\n\n```\nsondehub.Stream(sondes=["serial number"], on_message=callback)\n```\nIf no `sondes` list is provided then all radiosondes will be streamed.\n\nOn message callback will contain a python dictonary using the [Universal Sonde Telemetry Format](https://github.com/projecthorus/radiosonde_auto_rx/wiki/SondeHub-DB-Universal-Telemetry-Format)\n\n\n```\nsondehub.Stream().add_sonde(serial)\nsondehub.Stream().remove_sonde(serial)\n```\n\nAdds or removes a radiosonde from the filter\n\nData license\n--\nData is provided under the [Creative Commons BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) license.\n\nExample Usage\n--\n\n```python\nimport sondehub\n\ndef on_message(message):\n    print(message)\n\ntest = sondehub.Stream(sondes=["R3320848"], on_message=on_message)\n#test = sondehub.Stream(on_message=on_message)\nwhile 1:\n    pass\n\n```\n\nCLI Usage\n```sh\n# all radiosondes\nsondehub\n# single radiosonde\nsondehub --serial "IMET-73217972"\n# multiple radiosondes\nsondehub --serial "IMET-73217972" --serial "IMET-73217973"\n#pipe in jq\nsondehub | jq .\n{\n  "subtype": "SondehubV1",\n  "temp": "-4.0",\n  "manufacturer": "SondehubV1",\n  "serial": "IMET54-55067143",\n  "lat": "-25.95437",\n  "frame": "85436",\n  "datetime": "2021-02-01T23:43:57.043655Z",\n  "software_name": "SondehubV1",\n  "humidity": "97.8",\n  "alt": "5839",\n  "vel_h": "-9999.0",\n  "uploader_callsign": "ZS6TVB",\n  "lon": "28.19082",\n  "software_version": "SondehubV1",\n  "type": "SondehubV1",\n  "time_received": "2021-02-01T23:43:57.043655Z",\n  "position": "-25.95437,28.19082"\n}\n....\n\n```\n\n\nOpen Data Access\n==\n\nA basic interface to the Open Data is a available using `sondehub.download(serial=None, datetime_prefix=None)`\n\n```\nimport sondehub\nframes = sondehub.download(datetime_prefix="2018-10-01")\nframes = sondehub.download(serial="serial")\n```',
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/projecthorus/pysondehub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
