from setuptools import setup, find_packages

with open('readme.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='deepobfuscode',
    version='1.0.0',
    description='Automated source code obfuscation',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Siddhartha Datta',
    author_email='siddhartha.datta@cs.ox.ac.uk',
    keywords=['obfuscation', 'seq2seq'],
    url='https://github.com/dattasiddhartha/DeepObfusCode',
    download_url='https://pypi.org/project/deepobfuscode/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)