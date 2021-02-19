from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='watchtower_logging',
    version='0.1.0',
    description='Logging to WatchTower instance',
    license='MIT',
    packages=find_packages(),
    author='Jacob Noordmans',
    author_email='jacob@graindataconsultants.com',
    keywords=['WatchTower']
)

install_requires = [
    'requests',
    'python-json-logger',
    'pytz'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)