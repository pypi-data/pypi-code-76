import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="kodland_sso_server",  # Replace with your own username
	version="0.3.0",
	author="Dmitry Shoytov",
	author_email="shoytov@gmail.com",
	description="Django sso server package for Kodland",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="",
	packages=setuptools.find_packages(),
	install_requires=[
		'django==2.0.1',
		'djangorestframework==3.11.2',
		'django-rest-swagger==2.2.0',
		'pika==1.2.0'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
