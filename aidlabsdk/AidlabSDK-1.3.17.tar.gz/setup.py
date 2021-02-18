
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
   long_description = fh.read()

with open("LICENSE.md", "r") as fh:
   license = fh.read()

setup_args = dict(
    name='AidlabSDK',
    version='1.3.17',
    description='SDK tools to integrate Aidlab into your projects.',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license=license,
    packages=find_packages(),
    install_requires=['bleak==0.10.0'],
    author='Aidlab',
    author_email='contact@aidlab.com',
    keywords=['Biofeedback', 'Aidlab', 'chest strap', 'sdk', 'signals', 'biosignals', 'heart rate', 'ecg'],
    url='https://www.aidlab.com',
    include_package_data=True
)

if __name__ == '__main__':
    setup(**setup_args)
