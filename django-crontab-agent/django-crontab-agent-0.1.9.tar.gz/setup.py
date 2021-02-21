# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="django-crontab-agent",
    version="0.1.9",
    description="Agent for django-crontab-manager. Installed the agent on the target server. The agent will sync  settings from the manager and update the crontab file every minutes. Note: It is an agent implementation of django-crontab-manager server.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['django extensions'],
    install_requires=requires,
    packages=find_packages("."),
    entry_points={
        'console_scripts': [
            'django-crontab-agent = django_crontab_agent.cli:agent',
        ]
    },
)