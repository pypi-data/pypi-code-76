import setuptools
with open(r'D:\Python\Pypi-uploader\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='PyFastConfig',
	version='1.1',
	author='Super_Zombi',
	author_email='super.zombi.yt@gmail.com',
	description='Fast creation and reading of files on Python with configurations.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/PyFastConfig',
	packages=['PyFastConfig'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)