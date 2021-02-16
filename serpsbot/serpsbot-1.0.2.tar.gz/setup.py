from setuptools import setup

setup(name='serpsbot',
	version='1.0.2',
	description='SerpsBot Python API wrapper. Get Google SERPs as JSON using SerpsBot API.',
	author="SerpsBot",
	author_email="sales@serpsbot.com",
	url="https://github.com/serpsbotapi/serpsbot-python",
	license="MIT",
	packages=[
		'serpsbot'
	],
	install_requires=[
		'requests'
	]
)