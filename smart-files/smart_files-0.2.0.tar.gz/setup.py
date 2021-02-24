# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coverage>=5.4,<6.0',
 'pytest-watch>=4.2.0,<5.0.0',
 'pytest>=6.2.2,<7.0.0',
 'python-crontab>=2.5.1,<3.0.0']

entry_points = \
{'console_scripts': ['smart-files = scripts.smart_files:smart_files']}

setup_kwargs = {
    'name': 'smart-files',
    'version': '0.2.0',
    'description': 'Automatically sort files by type in your downloads folder',
    'long_description': '# smart-files\n### Ashley Casimir, Sean Hawkins, Ben Hill, Karlo Mangubat\n\n## Instructions\n\n### Before We Start\n\nThis module utilizes `crontab`.\n\nFor Mac ver. 10.15.6 or greater:\n\n1. In order for this module to work properly, we need to grant full-disk access for `cron` upon installation\n\n2. Open Finder and on the top-left corner of the screen, click "Go" and select “Go to folder"\n\n3. Insert this to location: `/usr/sbin/cron` \n\n4. Select "Go" and locate `cron`\n\n5. Go to System Preferences and then to Security and Privacy\n\n6. Navigate to Full Disk Access and click the lock at the bottom left to unlock\n\n7. Drag `cron` from finder to the list of apps in Full Disk Access. Ensure `cron` is checked prior to closing the window. \n\n### Quick Start\n1. On your Terminal, navigate to the smart-files repo\n2. Run `poetry install`\n3. Run `poetry run smart-files` to display options\n\n### Add Scheduled Sorting Job\n1. Run `poetry run smart-files cron` to display job frequency options. The result is displayed below:\n```\nOptions:\n-m, --minutes  Will create a cron job for Smart-files to run every minute\n-h, --hour     Will create a cron job for Smart-files to run every hour\n-d, --day      Will create a cron job for Smart-files to run once every day\n-o, --month    Will create a cron job for Smart-files to run once a month\n--help         Show this message and exit.\n```\n2. Add the desired command at the end of `poetry run smart-files cron`\n3. For example, the command for running smart-files every minute would be `poetry run smart-files cron -m`\n4. Verify that the crontab job exists by running the command `crontab -l`\n> Note: Running a new smart-files job will overwrite the old smart-files job.\n### Sort Files\nTo sort files on an ad hoc basis:\n1. Run `poetry run smart-files run`\n2. Check Downloads folder and verify that the files are sorted to their respective folders. \n\n### Display Unsorted Files\nTo display unsorted files:\n1. Run `poetry run smart-files show-files`\n2. The files displayed are coming from the Downloads folder, excluding the folders smart-files creates\n\n\n## Preparations\n\n1. Summary of idea:\n\n- An app that takes all downloaded files and automatically puts them in the proper folder based on the file type. For example, an image (.jpg or .png) would automatically go into the images folder from downloads.\n\n2. Problem or pain point:\n\n- Are you tired of having to organize your downloads manually? Do you just not have time for it? Our app will do this automatically so that the only thing you need to do is download. Our app will automatically filter it into the correct directory.\n\n3. Minimum Viable Product (MVP) definition:\n\n- We will be able to _easily_ prove that common file types for images, videos, standard docs, and software downloads will automatically transfer from the downloads folder to the correct directory. Our app should be able to do this in a very short amount of time to display seamless functionality. In addition, the app should be able to work on all our individual machines. This app will be added as a pip module. This will involve at least:\n  - Creating a setup file to help new users download and use as intended.\n  - Creating various forms of documentation.\n  - Creating a license.\n  - Creating a source distribution (meta-data) to ensure program works on everyone’s computer. -Testing and publishing package on PyPl.\n\n## Domain model\n- User will have the option to pip install\n\n![domain](img/domain.png)\n## Wire frame\n![download](img/top-level-wf.png)\n![software](img/software-wf.jpeg)\n![document](img/doc-wf.jpeg)\n![image](img/img-wf.jpeg)\n![other](img/other-wf.jpeg)',
    'author': 'BEN',
    'author_email': 'benjamin.hill28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ashcaz/smart-files/tree/main',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
