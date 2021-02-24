from setuptools import setup, find_packages


version = "1.0.8.1"

setup(
    name="pge",
    version=version,
    description="Graph modeling, EI estimation and analysis",
    author="Maxim Ryzhov",
    author_email="ryzhov@phystech.edu",
    license="MIT",
    packages=find_packages(),
    url="https://gitlab.com/BoBeni/PGEstimate",
    install_requires=["numpy", "scipy", "networkx", "pandas", "scipy", "mcg"],
    zip_safe=False,
)
