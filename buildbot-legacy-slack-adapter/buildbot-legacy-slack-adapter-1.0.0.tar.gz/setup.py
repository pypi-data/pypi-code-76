from setuptools import setup

import buildbot_legacy_slack_adapter

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="buildbot-legacy-slack-adapter",
    version="1.0.0",
    description="Plugin for integration with Slack on BuildBot 1.3.0.",
    author="Marc Leonardi",
    author_email="marc@goodbarber.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["buildbot_legacy_slack_adapter"],
    install_requires=["buildbot==1.3.0"],
    entry_points={
        "buildbot.reporters": [
            "SlackStatusPush = buildbot_legacy_slack_adapter.reporter:SlackStatusPush"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)