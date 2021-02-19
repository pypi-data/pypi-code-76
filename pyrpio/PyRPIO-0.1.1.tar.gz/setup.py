# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrpio']

package_data = \
{'': ['*'], 'pyrpio': ['lib/*']}

setup_kwargs = {
    'name': 'pyrpio',
    'version': '0.1.1',
    'description': 'Python-wrapped RPIO',
    'long_description': "# PyRPIO\n\n![./icon.png](./icon.png)\n\nA Python 3 addon which provides high-speed access to the Raspberry Pi GPIO interface, supporting regular GPIO as well as i²c, PWM, SPI, and MDIO.\n\nThis package is inspired by [node-rpio](https://github.com/jperkin/node-rpio) which is a node.js addon.\n\n![PyPI](https://img.shields.io/pypi/v/pyrpio)\n\n## Compatibility\n\n- Raspberry Pi Models: A, B (revisions 1.0 and 2.0), A+, B+, 2, 3, 3+, 3 A+, 4, Compute Module 3, Zero.\n- Python 3.7+\n\n## Install\n\nInstall the latest from PyPi:\n\n> `pip install pyrpio`\n\n## Supported Interfaces\n\n- GPIO\n- PWM\n- I2C\n- MDIO\n- SPI\n\n## Examples\n\n```python\nfrom pyrpio.i2c import I2C\nfrom pyrpio.mdio import MDIO\nfrom pyrpio.i2c_register_device import I2CRegisterDevice\n### I2C Operations ###\n\ni2c_bus = i2c.I2C('/dev/i2c-3')\ni2c_bus.open()\n\ni2c_bus.set_address(0x50)\n\ni2c_bus.read_write(data=bytes([0x23]), length=1)\n\ni2c_dev = I2CRegisterDevice(bus=i2c_bus, address=0x50, register_size=1, data_size=1)\n\n# Read register\nval = i2c_dev.read_register(register=0x23)\n\n# Read sequential registers\nvals = i2c_dev.read_register_sequential(register=0x23, length=4)\n\n# Close up shop\ni2c_bus.close()\n\n### MDIO Operations ###\n\n# Create bus using GPIO pins 23 and 24 (bit-bang)\nmdio_bus = mdio.MDIO(clk_pin=23, data_pin=24, path='/dev/gpiochip0')\nmdio_bus.open()\n\n# Read register 0x10 from device 0x30 (CLAUSE-45)\nmdio_bus.read_c45_register(0x30, 0x00, 0x10)\n\n# Read register set from device 0x30 (CLAUSE-45)\nmdio_bus.read_c45_registers(0x30, 0x00, [0,1,2,3,4])\n\n# Close up shop\nmdio_bus.close()\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Maintainers\n\n- [Samtec - ASH](https://samtec-ash.com)\n",
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samtec-ASH/pyrpio',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
