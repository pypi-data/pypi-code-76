from distutils.core import setup
setup(
  name = 'howami',         
  version = '0.1',      
  license='MIT',        
  description = 'You always ask your system \"whoami\", ask it "howami" for a change!',   
  author = 'Ghosty',             
  download_url = 'https://github.com/Ghostishghosty/howami/archive/0.1.tar.gz',    
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
