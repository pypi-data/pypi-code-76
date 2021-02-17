import setuptools
with open("README.md","r",encoding='utf-8')as fh:
	long_description=fh.read()
setuptools.setup(
	name="download_file",
	version="0.2",
	author="CNlong",
	author_email="T3464356490@outlook.com",
	description="download_file",
	long_descrtiption="You can use it to download_file,How to use it README.md",
	long_description_content_type="text/markdown",
	url="https://github.com/CNlong-Py/Pythonlibrarty.git",
	packages=setuptools.find_packages(),
	classifiers=[       
		"Programming Language :: Python :: 3",
       		 "License :: OSI Approved :: MIT License",
       		 "Operating System :: OS Independent",
   		 ],
)
		