"""
Flask-mongobit
---------------

MongoBit support in Flask
"""
import io
import os.path
from setuptools import setup

work_dir = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(work_dir, "flask_mongobit/__init__.py")

version = ""
with io.open(fp, encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__ = "):
            version = line.split("=")[-1].strip().replace("'", "")
            break

setup(
    name="flask-mongobit",
    version=version.replace('"', ""),
    url="https://github.com/lixxu/flask-mongobit",
    license="BSD",
    author="Lix Xu",
    author_email="xuzenglin@gmail.com",
    description="MongoBit support in Flask",
    long_description=__doc__,
    packages=["flask_mongobit"],
    zip_safe=False,
    platforms="any",
    install_requires=["MongoBit"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
