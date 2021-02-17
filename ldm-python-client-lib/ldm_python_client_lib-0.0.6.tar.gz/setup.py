from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='ldm_python_client_lib',
    version='0.0.6',
    description=' Python client side functions for working with LDM framework.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(include=['logger', 'logger.*']),
    author='sergejsrk',
    author_email='rikachovs@gmail.com',
    keywords=['LDM', 'Python 3', 'ML life cycle'],
    url='https://github.com/IMCS-DL4media/LDM_midterm',
    download_url='https://pypi.org/project/ldm_python_client_lib/'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
