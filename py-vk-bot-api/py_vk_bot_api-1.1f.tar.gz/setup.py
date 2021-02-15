from distutils.core import setup
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

def packages():
    pipfile = Project(chdir=False).parsed_pipfile
    return convert_deps_to_pip(pipfile['packages'], r=False)

setup(
    name='py_vk_bot_api',
    version='1.1',
    author='Airkek',
    author_email='',
    description='Python vk.com API wrapper',
    url='https://github.com/Airkek/py_vk_bot_api/',
    packages=['py_vk_bot_api'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=packages()
)
