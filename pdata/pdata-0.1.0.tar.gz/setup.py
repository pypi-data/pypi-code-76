from setuptools import setup

with open('requirements.txt') as req_file:
    requirements = req_file.readlines()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Oleksandr Semeniuta",
    author_email='oleksandr.semeniuta@gmail.com',
    name='pdata',
    version='0.1.0',
    packages=['pdata'],
    license='BSD license',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
)
