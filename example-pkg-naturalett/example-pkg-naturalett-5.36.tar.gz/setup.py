import setuptools, os
from os.path import dirname, relpath


with open("packaging_tutorial/README.md", "r") as fh:
    long_description = fh.read()





def do_setup() -> None:
    """
    Perform the Liminal package setup.
    """
    setup_kwargs = {}

    def local_scheme(version):
        return ""

    def test_pypi_publish() -> None:
        """
        When github action test-pipy-publish.yml got triggered then increment the release version.
        i.e. release vesion + dev0
        """
        if os.environ.get('TEST_PYPI_PUBLISH') == 'True':
            setup_kwargs['use_scm_version'] = {'local_scheme': local_scheme}
            setup_kwargs['setup_requires'] = ['setuptools_scm']
    test_pypi_publish()
    setuptools.setup(
        name="example-pkg-naturalett", # Replace with your own username
        version=os.environ.get("LIMINAL_BUILD_VERSION", os.environ.get('LIMINAL_VERSION', None)),
        author="Example Author",
        author_email="author@example.com",
        description="A small example package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/pypa/sampleproject",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        **setup_kwargs
    )

if __name__ == "__main__":
    do_setup()