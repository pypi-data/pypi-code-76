import sys
import subprocess

def __getattr__(name):  # python 3.7+, otherwise define each script manually
    name = name.replace('_', '-')
    subprocess.run(
        ['python', '-u', '-m', name] + sys.argv[1:]
    )  # run whatever you like based on 'name'