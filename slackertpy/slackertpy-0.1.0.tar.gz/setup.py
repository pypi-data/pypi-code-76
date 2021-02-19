import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="slackertpy",
    version="0.1.0",
    author="Maciej Olko",
    description="Crete and send Slack messages and alerts through a webhook",
    url="https://github.com/braze-inc/braze-growth-shares-slackertpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    tests_require=[
        'pytest'
    ]
)
