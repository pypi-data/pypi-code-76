from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='emailCrawlerPY',
  version='2.0',
  description='Small tool to crawl email from given websites',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jacopin Guillaume',
  author_email='guillaume.jacopin@sts-sio-caen.info',
  license='MIT', 
  classifiers=classifiers,
  keywords=['scrap', 'scrapper','scrapping','crawl','crawler','email','mail'],
  packages=['crawler'],
  include_package_data=True,
  install_requires=['beautifulsoup4 >= 4.9.3','PySimpleGUI','requests','lxml'],
  entry_points={
      "console_scripts":[
          "emailCrawlerPY=crawler.__main__:main"
      ]
  }
)
