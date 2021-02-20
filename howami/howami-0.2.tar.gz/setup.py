from distutils.core import setup
setup(
  name = 'howami' ,        
  version = '0.2',      
  license='MIT',        
  description = 'You always ask your system \"whoami\", ask it "howami" for a change!',   
  author = 'Ghosty',             
  #download_url = 'https://github.com/Ghostishghosty/howami/archive/0.2.tar.gz',   
  entry_points={
      'console_scripts' : [
          'howami = howami:main'
          ]
      },
  py_modules=['howami'],
  keywords = ['whoami', 'howami'],   
  install_requires=[            
          'psutil',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
  ],
)
