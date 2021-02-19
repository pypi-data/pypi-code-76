#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
setup(
  name = 'speech_recognition_python',         # How you named your package folder (MyLib)
  packages = ['speech_recognition_python'],   # Chose the same as "name"
  version = '3.9.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'speechrecognition using pretrained model',   # Give a short description about your library
  author = 'adam',                   # Type in your name
  author_email = 'admin@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/amanindia9',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/amanindia9/speech_recognition_python/archive/3.9.4.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyaudio',
          'speechrecognition',
          'google-trans-new',
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
  ],
)

