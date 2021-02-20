# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paper_animator']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.13,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pymupdf>=1.18.8,<2.0.0',
 'pypng>=0.0.20,<0.0.21',
 'scikit-video>=1.1.11,<2.0.0',
 'tqdm>=4.57.0,<5.0.0']

entry_points = \
{'console_scripts': ['paper-animator = paper_animator:main']}

setup_kwargs = {
    'name': 'paper-animator',
    'version': '0.0.1',
    'description': 'Animate a version-controlled PDF/LaTeX paper!',
    'long_description': "# paper-animator\n\nAnimate the progression of your version-controlled paper <3\n\n## Installation\n\n```\npip install paper-animator\n```\n\nor from source, with poetry\n\n```\ngit clone https://github.com/sneakers-the-rat/paper-animator\ncd paper-animator\npoetry install\n```\n\n## Usage\n\nSimplest case, just point it to a .pdf file in some git repository :)\n\n```\npaper-animator /some/repo/paper.pdf\n```\n\nThat method uses the .pdf checked in for each commit in the `main` branch.\nIf you point it to a .tex file, it will attempt to build it for you! (experimental)\n\n```\npaper-animator /some/repo/paper.tex --latex_builder pdflatex\n```\n\nUse a repo that's not local! Give the file as a path relative to the root\n\n```angular2html\npaper-animator subdirectory/paper.pdf --repo https://github.com/username/example_repo --branch main\n```\n\nSee `paper-animator --help` for all options\n\n```\n$ paper-animator --help\nusage: paper-animator [-h] [--output OUTPUT] [--repo REPO] [--branch BRANCH] [--tmp_dir TMP_DIR] [--latex_builder {pdflatex,xetex}] [--frame_duration FRAME_DURATION] [--video_fps VIDEO_FPS]\n                      [--resolution RESOLUTION] [--grid_shape GRID_SHAPE] [--dont_cleanup]\n                      input\n\nConvert a version controlled paper to a video!\n\npositional arguments:\n  input                 Input file, a .pdf or .tex file!\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --output OUTPUT       Output video file, if absent, input with .mp4 extension, default: None\n  --repo REPO           URL to a git repository to clone, if absent, get repo from input file, default: None\n  --branch BRANCH       Which branch to use, default: main\n  --tmp_dir TMP_DIR     Temporary directory to use, otherwise create one in ~/, default: None\n  --latex_builder {pdflatex,xetex}\n                        if input is a latex file, which builder to use with latexmk, default: pdflatex\n  --frame_duration FRAME_DURATION\n                        Duration (in s) to show each commit, default: 1\n  --video_fps VIDEO_FPS\n                        fps of output video, default: 30\n  --resolution RESOLUTION\n                        Resolution of plots, default: (1920, 1080)\n  --grid_shape GRID_SHAPE\n                        Manually override (rows,cols) of figure layout, default: None\n  --dont_cleanup        Delete temporary folder after completion\n```\n",
    'author': 'sneakers-the-rat',
    'author_email': 'JLSaunders987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakers-the-rat/paper-animator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
