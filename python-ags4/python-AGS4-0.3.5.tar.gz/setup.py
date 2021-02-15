# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_ags4']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'defusedxml>=0.6.0,<0.7.0',
 'openpyxl>=3.0,<4.0',
 'pandas>=1.0,<2.0',
 'rich>=9.0,<10.0']

entry_points = \
{'console_scripts': ['ags4_cli = python_ags4.ags4_cli:main']}

setup_kwargs = {
    'name': 'python-ags4',
    'version': '0.3.5',
    'description': 'A library to read and write AGS4 files using Pandas DataFrames',
    'long_description': '# python-ags4\nA library to read and write AGS4 files using Pandas DataFrames\n\n## Installation\n\n```bash\npip install python-ags4\n```\n\n## Introduction\n`python-ags4` is a library of functions that lets a user import [AGS4](http://www.agsdataformat.com/datatransferv4/intro.php) files to a collection of Pandas DataFrames. The data can be analyzed, manipulated, and updated using Pandas and then exported back to an AGS4 file.\n\n## Examples\n\n#### Import module:\n```python\nfrom python_ags4 import AGS4\n```\n\n#### Import data from an AG4 file:\n```python\ntables, headings = AGS4.AGS4_to_dataframe(\'/home/asitha/Projects/python-AGS4/tests/test_data.ags\')\n```\n* *tables* is a dictionary of Pandas DataFrames. Each DataFrame contains the data from a *GROUP* in the AGS4 file. \n* *headings* is a dictionary of lists. Each list has the header names of the corresponding *GROUP*\n\nAll data are imported as text so they cannot be analyzed or plotted immediately. You can use the following code to convert all the numerical data in a DataFrame from text to numeric.\n\n```python\nLOCA = AGS4.convert_to_numeric(tables[\'LOCA\'])\n```\n\nThe `AGS4.convert_to_numeric()` function automatically converts all columns in the input DataFrame with the a numeric *TYPE* to a float. (*Note: The UNIT and TYPE rows are removed during this operation as they are non-numeric.*)\n\n#### Export data back to an AGS4 file:\n\n``` python\nAGS4.dataframe_to_AGS4(tables, headings, \'/home/asitha/Documents/output.ags\')\n```\n\nA DataFrame with numeric columns may not get exported with the correct precision so they should be converted back to formatted text. The ```AGS4.convert_to_text()``` function will do this automatically if an AGS4 dictionary file is provided with the necessary UNIT and TYPE information. Numeric fields in the DataFrame that are not described in the dictionary file will be skipped with a warning.\n```python\nLOCA_txt = AGS4.convert_to_text(LOCA, \'DICT.ags\')\n```\n\nTables converted to numeric using the ```AGS4.convert_to_numeric()``` function should always be converted back to text before exporting to an AGS4 file. (*Note: The UNIT and TYPE rows will be added back in addition to formatting the numeric columns.*) \n\n## Command Line Interface ##\n\nA cli tool was added in version 0.2.0. It should be available from the terminal (or on the Anaconda Powershell prompt in Windows) after running ```python pip install python-ags4>=0.2.0```\n\nIt does not yet have the full functionality of the library, but it does provide a quick and easy way to convert .ags files to Excel spreadsheets (.xlsx) and back. The data can be easily edited in a spreadsheet and then converted back a .ags file. The TYPE values for numeric columns can be changed in the spreadsheet and the data will be automatically reformatted correctly when converted back to .ags, as long as all values in a column are numbers. Any supposedly numeric columns with text entries will be skipped with a warning message.\n\n*(Note: All data is imported to the spreadsheet as text entries so any column that should be reformatted should be explicitly converted to numbers in Excel.)*\n\n[![asciicast](https://asciinema.org/a/O7zhgGqWlobK8Hiyqrx3NGtaf.svg)](https://asciinema.org/a/O7zhgGqWlobK8Hiyqrx3NGtaf)\n\nA checking tool is available as of version 0.3.0 and it can be used to make sure that the file conforms to the AGS4 rules. The tool has been tested in both bash and Powershell.\n\n[![asciicast](https://asciinema.org/a/OOVN1rtqpvggzt9ZlHAlLBb6M.svg)](https://asciinema.org/a/OOVN1rtqpvggzt9ZlHAlLBb6M)\n\n## Graphical User Interface using *pandasgui*\n\nThe output from `python-ags4` can be directly used with [`pandasgui`](https://github.com/adamerose/pandasgui) to view and edit AGS4 files using an interactive graphical user interface. It also provides funtionality to plot and visualize the data.\n\n```python\nfrom pandasgui import show\n\ntables, headings = AGS4.AGS4_to_dataframe(\'/home/asitha/Projects/python-AGS4/tests/test_data.ags\')\ngui = show(**tables)\n```\n\n<img src="https://github.com/asitha-sena/python-ags4/blob/master/tests/pandasgui_screenshot.PNG" width=800>\n\nAny edits made in the GUI can be saved and exported back to an AGS4 file as follows:\n\n```python\nupdated_tables = gui.get_dataframes()\n\nAGS4.dataframe_to_AGS4(updated_tables, headings, \'/home/asitha/Documents/output.ags\')\n```\n',
    'author': 'Asitha Senanayake',
    'author_email': 'asitha.senanayake@utexas.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asitha-sena/python-AGS4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
