# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvdastwrapper']

package_data = \
{'': ['*'],
 'cvdastwrapper': ['templates/*',
                   'templates/assets/images/*',
                   'templates/assets/images/charts/*',
                   'templates/assets/styles/*']}

install_requires = \
['cvdast']

entry_points = \
{'console_scripts': ['cvdast-wrapper = cvdastwrapper.entry:main']}

setup_kwargs = {
    'name': 'cvdastwrapper',
    'version': '1.48.19',
    'description': 'This is a wrapper around CVDAST',
    'long_description': '\n--------- ReadMe:\n\n1. About ----\n\n* Python Runtime and Package Installation\nFirst of it, it is assumed that python3 and pip3 are installed. And\ncvdastwrapper package is installed by pip3. The python3 command can sometimes\njust be "python" if your default python installation is version 3 or above.\nPlease run "python --version" to find out. If you are running python 3 or above\nby default, please simply substitute the "python3" commands in examples provided\nin the remainder of this document.\n\nEnsure cvdast is available and up-to date, please run:\n   pip3 install -U cvdast\n   \nTo ensure cvdastwrapper is up-to-date, please run:\n   pip3 install -U cvdastwrapper\n\n* Test Directory\nCreate a Test directory where the spec files and config file can be placed. \nPlease feel free to rename the test directory. The subdirectory structure is\nimportant for the test run. All files generated will be put under the test directory.\n\n* Config:\nThe file cv_config.yaml is used to specify the authentication API endpoint and\nthe credentials to get the access token which is used to fuzz other APIs.\n \nThere will be information such as the URL of your test application (API endpoint),\nthe list of the fuzz attacks to try etc. in the cv_config.yaml which can be customized\nas per user environment. The same file contains all of the custom variables one needs\nto change. Current values are provided as examples. \n\nIn the Test directory create a folder called \'specs\' and place all the APIspecs (JSON\nversion only) here.\n \nAfter the test is complete (details in sections below), the summary-<timestamp>.html\nfile will contain pointers to all the test results. In addition, a file called\nfordev-apis.csv is generated. This is a highlevel summary for consumption of a\ndev team. It highlight just the API endpoints that seem to "fail" the test, ie.\nresponding positively instead of rejecting the fuzz calls. Please feel free to\nimport such CSV report to a spreadsheet. \n\nThe test results are stored in\n    results\n    results/perapi\n    results/perattack\n\nTest can run for a long time, so one can adjust the spec and the\ncollection of attacks in cv_config.yaml to stage each run. Test results\nof different test will not over-write each other. You can regenerate\ntest report after the test run.\n\n2. Generate fuzzing test for all the specs ----\n\nWith a given cvdast version and a set of specs, you need to only run\nthis once.\n\ncvdastwrapper --generate-tests \n\nA successfully run fuzzallspecs will generate as output a list of spec\ntitle names (taken from the spec\'s title) that can be used to update runall.py\nlist for test control (later 4. Control test)\n\n3. Running Tests -----------\n\nTo start the tests execute below command: \n\n cvdastwrapper test\n\nAbove cvdastwrapper also takes a "regen" argument. Regen will tells it not to\nrun the long test, but just run the cloudVectorDAST.generate_fuzz_report to\nagain generate the report (it copies the saved report.json from results\ndirectory)\n\nIt creates a summary-<timestamp>.html in the test. It contains tables allowing convenient\naccess to all the reports\n\nResults are saved in a directory called results\n\n  results\n    results/perapi\n    results/perattack\n\nAfter the test is finished you can find subdirectories with the Spec names under\neach of these results directories.\nThere are .html files that are the report html pointed to by the summary.\n\nUnder the perapi directory there are files that are named after the API\nname (chopped from the test directory long "for_fuzzing.py" name). The\nreport.json of the test run is saved with <apiname>-report.json',
    'author': 'Bala Kumaran',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
