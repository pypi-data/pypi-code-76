# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=2.0,<3.0',
 'PyYAML>=5.1,<6.0',
 'bottle>=0.12.13,<0.13.0',
 'lxml>=4.6.2,<5.0.0',
 'mdx_outline>=1.3.0,<2.0.0',
 'nose>=1.3.7,<2.0.0',
 'openpyxl>=2.6,<3.0',
 'plantuml-markdown>=3.4.0,<3.5.0',
 'python-markdown-math>=0.6,<0.7',
 'requests>=2.0,<3.0',
 'six']

setup_kwargs = {
    'name': 'portableqda',
    'version': '0.1.1',
    'description': 'import/export QDC and QDPX files for Qualitative Data Analysis (CAQDAS) Software, conforming to the XML-based REFI-QDA Standard (https://www.qdasoftware.org)',
    'long_description': '# portableQDA\n\nportableQDA is package for import/export of information according to REFI-QDA Standard:\n\n- Codebooks (QDC files)\n- Projects (QDPX files, not yet implemented)\n\nExchange formats [QDC and QDPX](https://www.qdasoftware.org/wp-content/uploads/2019/09/REFI-QDA-1-5.pdf) are:\n  - suitable for structured archiving of any kind of files, including:\n    + personal corpus of information analysis (coding, cites, comments) \n    + the source documents themselves (any arbitrary format, including office docs, PDF, html, audio) \n  - well-defined and maintained by the [REF-QDA working group](http://qdasoftware.org) \n  - supported and developed by a growing number of participants\n\nQDA stands for Qualitative Data Analysis, as known in social sciences. Related Wikipedia article states: “Qualitative research relies on data obtained by the researcher by first-hand observation, interviews, recordings, […]. The data are generally non-numerical. Qualitative methods include ethnography, grounded theory, discourse analysis […]. These methods have been used in sociology, anthropology, and educational research.”\n\n## Installation\n\n```bash\n# pip install portableqda\n```\n\n## Basic usage\n\n\n### testing the output format\n\n```bash\n# python -m portableqda\n```\n\nproduces an empty codebook file in your home directory, should be suitable for import by your CAQDAS software. \n\n### testing the input format\n\n- export a codebook from the QDA software of your choise\n- run the following script:\n```python\nimport portableqda\ncodebook = portableqda.codebookCls(output=None) #create a codebook, will export to the screen\ncodebook.readQdcFile(input="/path/to/your/exported.qdc")\ncodebook.writeQdcFile()\n```\n- no errors should ocurr, check the output for completeness\n\n\n### developing\n\n\n```python\nimport portableqda\n#look for output in system logging\n\ncodebook = portableqda.codebookCls(output="codebook_example.qdc") #create a codebook\n\n# create 3 codes and group them in two sets\nfor number in range(3):\n    error,errorDesc,code = codebook.createElement(elementCls=portableqda.codeCls,\n                                                name=f"code{number}",\n                                                sets=["set1","set2"])\n\ncodebook.writeQdcFile() # export the codebook as a REFI-QDA 1.5 compatible QDC file\n```\n\nLook for the file `codebook_example.qdc` at your home directory. You can see more of what\'s happening (portableQDA is a library thus not intended for direct use), inserting the following code where the comment "look for output in system logging" is, right after the `import portableqda` statement:\n\n```python\nimport logging\nhandler = logging.StreamHandler(sys.stdout)\nhandler.setLevel(logging.DEBUG)\nformatter = logging.Formatter(\'%(name)s - %(levelname)s - %(message)s\')\nhandler.setFormatter(formatter)\nportableqda.log.addHandler(handler)\nportableqda.log.setLevel(logging.DEBUG)\n```\n\nSomething like this will be shown:\n\n ```log\n portableqda.refi_qda - DEBUG - tree created, root node: \'CodeBook\'. see REFI-QDA 1.5\nportableqda.refi_qda - INFO - output is C:\\Users\\X\\codebook_example.qdc\nportableqda.refi_qda - DEBUG - added code code0 to set set1 \nportableqda.refi_qda - DEBUG - added code code0 to set set2 \nportableqda.refi_qda - DEBUG - added code code1 to set set1 \nportableqda.refi_qda - DEBUG - added code code1 to set set2 \nportableqda.refi_qda - DEBUG - added code code2 to set set1 \nportableqda.refi_qda - DEBUG - added code code2 to set set2 \nportableqda.refi_qda - INFO - exporting as REFI-QDC  codebook to file: C:\\Users\\X\\codebook_example.qdc\n ```\n\n\n## Documentation\n\n## Contributing\n\n### Acknowledges\n\nLMXL: portableQDA relies on the excellent [lxml package](http://lxml.de) for the  underlying tree data structure and  XML handling\nREFI-QDA: [working group](http://qdasoftware.org) pushing interoperability and open standards\n\n\n\n## License\n\nGNU Lesser General Public License v3 (LGPLv3)',
    'author': 'Leandro Batlle',
    'author_email': 'Leandro.Batlle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/portableqda/portableQDA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
