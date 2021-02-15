from os.path import dirname, join

try:
    from setuptools import setup
except:
    from distutils.core import setup

def get_version(relpath):
    path = join(dirname(__file__), relpath)
    for line in open(path, "rb"):
        line = line.decode("utf-8")
        if "__version__" in line:
            return line.split('"')[1]

py_packages = [
    "hgext3rd.fastimport",
    "hgext3rd.fastimport.vendor.python_fastimport",
]

py_packagedir = {
    "hgext3rd": join(dirname(__file__), "hgext3rd")
}

py_versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4"

setup(
    name="hg-fastimport",
    version=get_version("hgext3rd/fastimport/__init__.py"),
    author="The hg-fastimport authors",
    maintainer="Roy Marples",
    maintainer_email="roy@marples.name",
    url="https://roy.marples.name/hg/hg-fastimport/",
    description="Mercurial extension for importing a git fast-import stream.",
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    keywords="hg git mercurial",
    license="GPLv2",
    packages=py_packages,
    package_dir=py_packagedir,
    python_requires=py_versions,
)
