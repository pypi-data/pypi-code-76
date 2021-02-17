from distutils.core import setup
setup(
  name = 'rgb_to_hex',         # How you named your package folder (MyLib)
  packages = ["."],   # Chose the same as "name"
  version = '0.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "BU KÜTÜPHANE 'TKİNTER' KÜTÜPHANESİNDE 'RGB' RENK KODLARINI KULLANABİLMEK İÇİN YAZILMIŞTIR",   # Give a short description about your library
  author = 'SAMET ERİLTER',                   # Type in your name
  author_email = 'sametbilal34@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/NexDen',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/NexDen/rgb_to_hex/archive/v0.0.4.tar.gz',    # I explain this later on
  keywords = ["RGB","HEX"],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
