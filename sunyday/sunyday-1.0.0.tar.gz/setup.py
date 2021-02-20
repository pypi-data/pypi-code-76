from setuptools import setup
setup(
  name = 'sunyday',		#* Your package will have this name
  packages = ['sunyday'],  #* Name the package again
  version = "1.0.0",        #* To be increased every time your change your library
  license = "MIT",          # Type of license. More here: https://help.github.com/articles/licensing—a-repository
  description = 'Weather forecast data',  		# Short description of your library
  author = "Richard de Graaf",            		# Your name
  author_email = 'richie.de.graaf@gmail.com',  	# Your email
  url = 'https://example.com',  				# Homepage of your library (e.g. gìthub or your website)
  keywords = ['weather', 'forecast', 'openweather'], 		# Keywords users can search on pypi.org
  install_requires=[      						# Other 3rd-party libs that pip needs to install
  'requests',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha', 		# either 13 — Alpha", "4 - Beta" or "5 - Production/Stable" as the current st
	'Intended Audience :: Developers', 		# who's audience for your library?
	'Topic :: Software Development :: Build Tools',
	'License :: OSI Approved :: MIT License', # type a licence again
	'Programming Language :: Python :: 3.5',  # Python versions that your library supports
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8',
  ],
)