from distutils.core import setup

setup(
	name='ShapeTest', 
	author="Joshua Raphael Fuentes",
	author_email="joshuarpf@gmail.com",
	version='0.1dev', 
	packages=['shapetest',],
	license='Creative Commons Attribution-Noncommercial-Share Alike license', 
	long_description=open('README.txt').read(), 
	entry_points={
		'console_scripts': [
			'test=shapetest:main'
		]
	}
)