import codecs
from setuptools import setup, find_packages
 

def read_file(filename, cb):
    with codecs.open(filename, 'r', 'utf8') as f:
        return cb(f)

classifiers  =  [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name = 'payUnit',
  version = '0.2.3',
  description = 'Python sdk for payUnit payments, including Mtn momo,Orange momo,Express Union',
  long_description = read_file('README.md', lambda f: f.read()) + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url = '',  
  author = 'SevenGps',
  author_email =  'info@sevengps.com',
  license = 'MIT', 
  classifiers = classifiers,
  keywords = 'payUnit, momo ,payment', 
  packages = find_packages(),
  install_requires = ['requests','uuid'] 
)
