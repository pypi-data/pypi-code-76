# https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#development-mode
import setuptools

setuptools.setup(
    name="multi-config",
    version="0.1.0",
    author="Evan Aranda",
    description="Python configuration from multiple sources",
    license="MIT",
    url="https://github.com/EvanAranda/multi-config",
    packages=setuptools.find_packages(
        include=['configuration', 'configuration.*'],
        exclude=['tests']
    )
)
