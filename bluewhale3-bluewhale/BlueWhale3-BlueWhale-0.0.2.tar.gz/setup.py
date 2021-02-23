from setuptools import setup, find_packages

VERSION = '0.0.2'

ENTRY_POINTS = {
    'orange3.addon': (
        'blue_whale = orangecontrib.blue_whale',
    ),
    'orange.widgets': (
        'BlueWhale = orangecontrib.blue_whale.widgets',
    )
}

CLASSIFIERS = (
    "Development Status :: 1 - Planning",
    "Environment :: X11 Applications :: Qt",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
)

LICENSE = "BlueWhale"

setup(name="BlueWhale3-BlueWhale",
      packages=find_packages(),
      version=VERSION,
      install_requires=[
            'requests~=2.25.1',
            'PyQt5~=5.15.2',
            'AnyQt~=0.0.11',
            'numpy~=1.19.5',
            'setuptools~=51.0.0',
            'bluewhale-canvas-core',
            'bluewhale-widget-base',
            'BlueWhale3',
            'python-i18n',
        ],
      description="蓝鲸大数据平台，提供教学数据与案例",
      url='https://bw.dashenglab.com/',
      license=LICENSE,
      author='大数据团队',
      author_email='dashenglab@163.com',
      classifiers=CLASSIFIERS,
      package_data={"orangecontrib.blue_whale.widgets": ["icons/*", "utils/*", "datasets/*", "*"],
                    "orangecontrib.blue_whale": ["*.py", "locale/*"]},
      entry_points=ENTRY_POINTS
      )