from setuptools import setup, find_packages


def read_version():
    with open("amz/data/VERSION", "r") as ver:
        return ver.readlines()[0]


setup(name="amz-tool",
      version=read_version(),
      author="AMZ Dev Admin",
      author_email="dev@amzracing.ch",
      description="AMZ Codebase Management Tool",
      url="https://bitbucket.org/amzracing/amz-tool",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3", "Development Status :: 4 - Beta", "Operating System :: POSIX :: Linux",
          "License :: Other/Proprietary License"
      ],
      python_requires='>=3.6',
      include_package_data=True,
      install_requires=[
          'pyyaml>=5.3.0', 'requests', 'pylint>=2.6.0', 'cpplint>=1.5.4', 'pre-commit>=2.9.3', 'yapf>=0.30.0',
          'argcomplete', 'packaging'
      ],
      scripts=['bin/amz'])
