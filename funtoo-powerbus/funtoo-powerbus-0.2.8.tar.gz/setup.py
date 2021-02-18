import setuptools

from subpop.pkg import Packager, SubPopSetupInstall

pkgr = Packager()

with open("README.rst", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="funtoo-powerbus",
	version="0.2.8",
	author="Daniel Robbins",
	author_email="drobbins@funtoo.org",
	description="Funtoo Power Management Framework",
	long_description=long_description,
	long_description_content_type="text/x-rst",
	url="https://code.funtoo.org/bitbucket/users/drobbins/repos/funtoo-powerbus/browse",
	scripts=["bin/funtoo-powerbus", "bin/funtoo-idled", "bin/powerstatus"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: POSIX :: Linux",
	],
	python_requires=">=3.7",
	install_requires=["aiohttp", "dbus-next", "colorama", "subpop >= 0.4.1", "pymongo", "pyyaml"],  # for bson
	packages=setuptools.find_packages(),
	data_files=pkgr.generate_data_files(),
	cmdclass={"install": SubPopSetupInstall},
)
