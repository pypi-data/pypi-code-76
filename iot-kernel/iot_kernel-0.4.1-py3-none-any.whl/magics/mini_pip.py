#!/usr/bin/env python3

import subprocess
import shlex
import os
import glob
import shutil


"""
Download (circuit/micropython) packages from PyPi to MCU lib folder.
"""

class Pip:

    def __init__(self, path):
        self.path = path

    def install(self, package):
        self.package = package
        target = self.lib_path
        cmd = f"pip install {package} -t {target} --upgrade --no-deps"
        self._shell(cmd)
        self._cleanup(f'{target}/**/*.egg-info')
        self._cleanup(f'{target}/**/*.dist-info')
        self._cleanup(f'{target}/**/__pycache__')

    def uninstall(self, package):
        path = os.path.join(self.lib_path, package)
        try:
            os.remove(path + ".py")
        except FileNotFoundError:
            try:
                shutil.rmtree(path)
            except FileNotFoundError:
                print("Not found:", package)

    def list_installed(self):
        for f in os.listdir(self.lib_path):
            print(f)

    @property
    def lib_path(self):
        return self.path

    def _shell(self, cmd):
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode().strip())
        if process.returncode != 0:
            raise Exception(f"pip: install of '{self.package}' failed")

    def _cleanup(self, pattern):
        files = glob.glob(pattern, recursive=True)
        for f in files:
            shutil.rmtree(f)

def install(package, path):
    pip = Pip(path)
    pip.install(package)

if __name__ == "__main__":
    path = os.path.expanduser(path.join("~/mcu/pip_test/lib"))
    pip = Pip(path)
    pip.list_installed()
    pip.install('adafruit-circuitpython-register')
    pip.install('adafruit-circuitpython-busdevice')
    pip.install('adafruit-circuitpython-bno055')
    print("all installed:")
    pip.list_installed()
    pip.uninstall('adafruit_bus_device')
    print("minus bus_device")
    pip.list_installed()
