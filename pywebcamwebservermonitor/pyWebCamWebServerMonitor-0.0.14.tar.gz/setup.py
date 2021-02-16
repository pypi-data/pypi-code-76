from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = list(open('requirements.txt', 'r'))

setup(
    name='pyWebCamWebServerMonitor',
    author="Andrei O.(andrei0x309)",
    version="0.0.14",
    include_package_data=True,
    author_email="andrei@flashsoft.eu",
    description="Webcam WebControl panel build with flask & vue to record / see live and other things designed for linux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.flashsoft.eu/python/flask-pyWebCamWebMonitor",
    keywords="webcam web control panel, webcam linux server, embedded webcam control, live streaming webcam, recording webcam",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pyWebCamMonitorCtl=pyWebCamWebServerMonitor.commands:commands_main',
        ]},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Framework :: Flask",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Multimedia",
    ],
    python_requires='>=3.6',
)
 