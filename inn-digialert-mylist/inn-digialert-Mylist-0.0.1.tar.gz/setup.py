import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()
f = open("requirement.txt")
requirements = [req.strip() for req in f]
f.close()

print(setuptools.find_packages())
setuptools.setup(
	name="inn-digialert-Mylist",
	version="0.0.1",
	author="SimpleAppDesigner",
	author_email="Sandeep1dimri@gmail.com",
	description="MyList api built in Flask and sqlite",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://bitbucket.org/Radio_fixed/sqliteforkarate/src/master/",
	classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
				 "Operating System :: OS Independent"],
	packages=setuptools.find_packages(),
	python_requires='>=3.6',
	install_requires=requirements,
)
