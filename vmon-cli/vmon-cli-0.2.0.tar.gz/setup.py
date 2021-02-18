from setuptools import setup, find_packages

from distutils.util import convert_path

long_description ="""
# vmon-cli

vmon-cli - CLI Viewer for Ibsen 512 USB interrogator


## Installation

```bash
# clone the repository
$ git clone git@github.com:codenio/vmon-cli.git

# move into tmon-cli folder
$ cd vmon-cli

# install requirements
$ pip install -r requirments.txt

# intall tmon
$ pip install .

# check installation
$ vmon --help
Usage: vmon [OPTIONS] COMMAND [ARGS]...

  vmon - I-Mon Spectrum Viewer and Exporter

Options:
  --help  Show this message and exit.

Commands:
  export  Export Processed I-Mon data read from <file>.csv into...
  plot    Plot the I-Mon data into graphs
```

### Usage

- vmon commands
    ```bash
    vmon --help
    Usage: vmon [OPTIONS] COMMAND [ARGS]...

      vmon - I-Mon Spectrum Viewer and Exporter

    Options:
      --help  Show this message and exit.

    Commands:
      export  Export Processed I-Mon data read from <file>.csv into...
      plot    Plot the I-Mon data into graphs
    ```
- plot sub command
    ```bash
    $ vmon plot --help
    Usage: vmon plot [OPTIONS] FILES...

      Plot the I-Mon data into graphs

    Options:
      -p, --path TEXT   path form which csv files are to be imported, default = .
      -t, --title TEXT  set custom title for the plot, default = .
      -n, --normalise   normalise the data before ploting
      -pk, --peaks      show peaks in the plot
      --help            Show this message and exit.
    ```

- export sub command
    ```bash
    $ vmon export --help
    Usage: vmon export [OPTIONS] [FILES]...

      Export Processed I-Mon data read from <file>.csv into <file>_vmon.csv
      files

    Options:
      -p, --path TEXT  path form which csv files are to be imported, default = .
      -n, --normalise  normalise the data before ploting
      -i, --inspect    inspect the plot before exporting
      --help           Show this message and exit.
    ```
"""

pkg_ns = {}

ver_path = convert_path('vmon/__init__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_ns)

setup(
    name = 'vmon-cli',
    version = pkg_ns['__version__'],
    description='CLI Viewer for Ibsen 512 USB interrogator',
    url='https://github.com/codenio/vmon-cli',
    author='Aananth K',
    author_email='aananthraj1995@gmail.com',
    license='GPL-3.0',
    packages = find_packages(exclude=[]),
    install_requires=[
        "click==7.1.2",
        "cycler==0.10.0",
        "DateTime==4.3",
        "kiwisolver==1.3.1",
        "matplotlib==3.3.3",
        "numpy==1.19.4",
        "pandas==1.1.5",
        "Pillow==8.0.1",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "pytz==2020.4",
        "scipy==1.5.4",
        "six==1.15.0",
        "zope.interface==5.2.0",
    ],
    entry_points = {
        'console_scripts': [
            'vmon = vmon.main:cli'
        ]
    },
    zip_safe=False,
    long_description_content_type="text/markdown",
    long_description=long_description,
)
