from distutils.core import setup
setup(
  name = 'Watt',         # How you named your package folder (MyLib)
  packages = ['Watt'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library is high-level, straightforward, and yet extremely powerful library for management and creation of objects of the tree data structure in general(general trees), binary trees, and binary search trees. It is loaded with simple classes and functions to help you grow as a programmer and make your work easier.',   # Give a short description about your library
  author = 'Kanav Bhasin',                   # Type in your name
  author_email = 'kanbhasin@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/CriticalQuizzicalBooleanValue',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/BleepLogger/CriticalQuizzicalBooleanValue/archive/main.zip',    # I explain this later on
  keywords = ['Data', 'Tree', 'Structure', 'Data Structure', 'Binary Tree', 'Binary Trees', 'Data Science', 'Coding', 'Good'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'wheel',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
  ],
)