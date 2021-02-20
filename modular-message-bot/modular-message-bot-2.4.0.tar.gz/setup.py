import os
import time

from setuptools import find_packages, setup

root_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))


def get_version() -> str:
    version_file = os.path.join(root_dir, 'VERSION_PYPI')
    if not os.path.isfile(version_file):
        return f"0.0.0b{int(time.time())}"
    return open(version_file).read().strip()


# We lock these in the requirements.txt file
install_requires = [
    "requests>=2.23.0",
    "python-dotenv>=0.13.0",
    "pyyaml>=5.4.1",
    "APScheduler>=3.6.3",
    "pyjq>=2.5.1",
    "elasticsearch>=7.10.1",
]

# Because we do not have a dev dependencies lock file, lock them here
dev_requires = [
    "pip-tools==5.5.0",
    "coverage==5.3.1",
    "flake8==3.8.4",
    "black==19.10b0",
    "pytest==6.2.1",
    "pytest-mock==3.5.1",
    "pygount==1.2.4",
    "isort==5.7.0",
    "twine==3.3.0",
    "pdoc==1.1.0",
    "mypy==0.800",
]

setup(
    name="modular-message-bot",
    description="Takes data from sources and sends them somewhere based on a schedule that is defined in YAML",
    long_description=open(f"{root_dir}/README.md").read().strip(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mage-sauce/programs/modular-message-bot",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
      "dev": dev_requires
    },
    python_requires=">=3.8.0",
    platforms="any",
    version=get_version(),
    author="Jeremy Sells",
    author_email="mrjeremysells@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
