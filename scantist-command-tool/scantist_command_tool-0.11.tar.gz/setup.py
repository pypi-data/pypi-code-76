from setuptools import find_packages, setup

requirement = [
    'requests',
]

setup(
    name='scantist_command_tool',
    version='0.11',
    author="scantist",
    packages=find_packages(),
    license='Scantist license 1.0',
    # include_package_data=True,
    package_data={'command_tool': ['*.ini', '*.md', '*.jar']},
    install_requires=requirement,
    entry_points={
        'console_scripts': [
            'scantist_cmd = command_tool.scantist_cmd:main',
            'scantist_auth = command_tool.authenticate:main',
        ]
    },
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    description="scantist command line tool."
)
