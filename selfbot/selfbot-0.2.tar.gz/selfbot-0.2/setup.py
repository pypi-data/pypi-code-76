from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.rst").read_text()

setup(
  name = 'selfbot',
  packages = ['selfbot'],
  version = '0.2',
  license='MIT',
  description = 'Epic exploit discord api wrapper',
  author = 'razu',                   # Type in your name
  long_description=README,
  long_description_content_type = "text/markdown",
  author_email = 'support@xyris.org',      # Type in your E-Mail
  url = 'https://github.com/rqzu/selfbot.py',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/rqzu/AuthGG/archive/main.tar.gz',    # I explain this later on
  keywords = ['selfbot', 'discord', 'discord-selfbot'],   # Keywords that define your package best
  classifiers=[
    'Programming Language :: Python :: 3.6',
  ],
)