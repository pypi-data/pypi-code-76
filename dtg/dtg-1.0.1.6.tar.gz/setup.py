from setuptools import setup, find_packages

version = "1.0.1.6"


setup(
    name="dtg",
    version=version,
    description="Heavy-tailed distribution analysis",
    author="Maksim Ryzhov",
    author_email="ryzhov@phystech.edu",
    license="MIT",
    packages=find_packages(),
    url="https://gitlab.com/BoBeni/DTG",
    install_requires=["numpy", "scipy", "statsmodels"],
    zip_safe=False,
)
