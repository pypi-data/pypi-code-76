from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'SampleModule',         # How you named your package folder
  packages = ['SampleModule'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description='Sample Python Module',
  long_description_content_type='text/markdown',  # This is important!
  author = 'Anton Bondar',                   # Type in your name
  author_email = 'anton.bondar@newsignature.com',      # Type in your E-Mail
  url = 'https://newsignature.com',   # Provide either the link to your github or to your website
  keywords = ['Python', 'Sample', 'Module'],   # Keywords that define your package best
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)