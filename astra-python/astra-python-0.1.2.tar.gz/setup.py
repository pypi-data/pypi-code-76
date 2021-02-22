import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('astra/version.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setuptools.setup(
    name="astra-python",
    version=version,
    keywords='api, client, astra, plaid, dwolla',
    author="Astra, Inc.",
    author_email="gil@astra.finance",
    description="Python SDK for the Astra API.",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstraFinance/astra-python",
    packages=setuptools.find_packages(exclude='tests'),
    package_data={'README': ['README.md']},
    include_package_data=True,
    install_requires=['requests>=2.2.0'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
