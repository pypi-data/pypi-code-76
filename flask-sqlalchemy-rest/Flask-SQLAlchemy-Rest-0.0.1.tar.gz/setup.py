from setuptools import setup 
import re

with open("flask_sqlalchemy_rest/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name = "Flask-SQLAlchemy-Rest",
    version = version,
    url = "https://github.com/qf0129/flask-sqlalchemy-rest",
    license='MIT',
    author='Qifei',
    author_email='qf0129@qq.com',
    description = "RESTFUL API with Flask and SQLALchemy",
    long_description = "RESTFUL API with Flask and SQLALchemy",
    packages = ['flask_sqlalchemy_rest'],
    include_package_data = True,
    platforms = "any",
    install_requires=["Flask>=1.0.3", "SQLAlchemy>=1.2"],
)
