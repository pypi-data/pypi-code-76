from setuptools import setup
try:
    about = open('README.md', 'r').read()
except FileNotFoundError:
    about = None

setup(
    name='py-maia',
    version='1.5',
    description="Let's code better",
    packages=['maia', ],
    long_description=about,
    license='MIT',
    author='Arorior',
    url='https://github.com/Arorior/maia',
    long_description_content_type='text/markdown',
    include_package_data=True,
)
