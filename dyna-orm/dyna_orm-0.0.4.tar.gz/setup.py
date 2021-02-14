from distutils.core import setup

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
  name = 'dyna_orm',         # How you named your package folder (MyLib)
  packages = ['dyna_orm', 'dyna_orm.db', 'dyna_orm.utils'],   # Chose the same as "name"
  version = '0.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A small and simplistic AWS dynamodb ORM',   # Give a short description about your library
  author = 'Jesus Alvarez',                   # Type in your name
  author_email = 'alv.mtz94@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jsgilberto/dyna_orm',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jsgilberto/dyna_orm/archive/v0.0.3.tar.gz',    # I explain this later on
  keywords = ['Dynamodb', 'AWS', 'ORM'],   # Keywords that define your package best
  install_requires=[
          'boto3==1.16.32'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)