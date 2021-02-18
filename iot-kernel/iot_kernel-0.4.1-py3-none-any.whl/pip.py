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

    def __init__(self, root_dir, project, output):
        self.root_dir = os.path.expanduser(root_dir)
        self.project = project
        self.output = output

    def install(self, package):
        target = self.lib_path
        self.output.ans(f"install {package} in {target}\n")
        cmd = f"pip install {package} -t {target} --upgrade --no-deps"
        self._shell(cmd)
        self._cleanup(f'{target}/*.dist-info')
        self._cleanup(f'{target}/**/__pycache__')
        self.output.ans('\n')

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
            self.output.ans(f)
            self.output.ans('\n')

    @property
    def lib_path(self):
        return os.path.join(self.root_dir, self.project, 'lib')

    def _shell(self, cmd):
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.output.ans(stdout.decode().strip())
        self.output.ans('\n')
        if stderr:
            self.output.err(f"ERROR: {stderr.decode().strip()}\n")
        if process.returncode != 0:
            self.output.err("INSTALL FAILED\n")

    def _cleanup(self, pattern):
        files = glob.glob(pattern, recursive=True)
        for f in files:
            shutil.rmtree(f)


class Output:
    def ans(self, str): print(str)
    def err(self, str): print(str)

if __name__ == "__main__":
    pip = Pip("~/mcu", "pip_test", Output())
    pip.list_installed()
    pip.install('adafruit-circuitpython-register')
    pip.install('adafruit-circuitpython-busdevice')
    pip.install('adafruit-circuitpython-bno055')
    print("all installed:")
    pip.list_installed()
    pip.uninstall('adafruit_bus_device')
    print("minus bus_device")
    pip.list_installed()
