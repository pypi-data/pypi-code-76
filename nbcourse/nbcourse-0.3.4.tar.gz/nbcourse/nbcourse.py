#!/usr/bin/env python3
"""
Define a NbCourse object containing:
    - class methods for building html pages and pdf book
    - Doit tasks defined in task_*() functions
"""

from pathlib import Path, PosixPath
import yaml
from doit.tools import create_folder, config_changed
from . import log
from .utils import update_material, clean_tree, get_file_list, update_dict, \
    zip_files
from .pages import HomePage, MarkdownPage
from .book import Book
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter, SlidesExporter
from .mydoit import MyDoitMain, ClassTaskLoader
import sys


DEFAULT_CONFIG_FILE = "nbcourse.yml"


class NbCourse:

    default_conf = {
        'theme': {
            'dir': 'theme/default',
            'material': ('css', 'img')
        },
        'nb': {
            'dir': '.',
            'timeout': 60,
            'material': ()
        },
        'pages': {
            'dir': 'pages',
            'home': 'index.html'
        },
        'book': {
            'titlepage': 'titlepage.tex',
            'file': None,
        },
        'local_reveal': False,
        'slug_title': 'course',
        'output_dir': 'build',
        'title': 'A course',
        'subtitle': None,
        'favicon': None,
        'picture': None,
        'authors': [],
        'chapter_preview_only': [],
        'license': None,
        'links': {'manual': {
            'title': 'Manual',
            'target': 'manual.html',
        }
        }
    }

    def __init__(self, user_conf=None):
        """Build from user_conf"""
        self.conf = self._get_config(user_conf)
        self.conf['template_path'] = Path(self.conf['theme']['dir'],
                                          'templates')
        for key in 'nb', 'theme':
            self.conf[key]['path'] = Path(self.conf[key]['dir'])
            self.conf[key]['material_paths'] = [
                self.conf[key]['path'] / Path(d)
                for d in self.conf[key]['material']
            ]
        self.conf['pages']['path'] = Path(self.conf['pages']['dir'])
        self.conf['output_path'] = Path(self.conf['output_dir'])
        if self.conf['local_reveal']:
            self.conf['reveal_path'] = Path(__file__).parent / \
                Path('reveal.js')
        self.notebooks = tuple(self.conf['nb']['path'].glob('*-*.ipynb'))
        if user_conf and not self.notebooks:
            log.error("""
No notebooks found!
1. Check 'nb:dir:' field in nbcourse.yml file.
2. Ensure that your notebooks are named using the pattern:
   - "01-my_first_chapter_name.ipynb",
   - "02-my_second_chapter_name.ipynb",
   - etc.
""")
            sys.exit()
        if self.conf['book']['file']:
            self.titlepage_path = self.conf['pages']['path'] / \
                self.conf['book']['titlepage']
            self.book = self.conf['output_path'] / self.conf['book']['file']
        else:
            self.titlepage_path = None
            self.book = None
        self.md_page_paths = list(self.conf['pages']['path'].glob('*.md'))
        self.html_pages = self._get_pages()  # homepage and documentation pages
        self.theme_files = [file for file in
                            self.conf['theme']['path'].glob('**/*')
                            if file.is_file()]
        self.htmls = []  # html export of notebooks
        self.slides = []  # reveal slide export of notebooks
        self.material = []  # additional material (pictures, etc.)
        self.chapter_zips = []

        self.executed_notebooks = [self._get_executed_nb_path(notebook)
                                   for notebook in self.notebooks]
        self.zip_file = self.conf['output_path'] / \
            Path(self.conf['slug_title']).with_suffix('.zip')

        # Instantiate notebook exporter
        self.html_exporter = HTMLExporter(template_name='classic')

        # Instantiate slide exporter
        self.slide_exporter = SlidesExporter()
        if self.conf['local_reveal']:
            self.slide_exporter.reveal_url_prefix = 'reveal.js'

    def _get_config(self, user_conf):
        """Get conf dict from default and user_conf"""

        def sanitize(user_conf_dict: dict):
            """
            Sanitize user_conf_dict: remove first level keys that are
            not present in default dict
            """
            for k in user_conf_dict:
                if k not in conf.keys():
                    log.warning(f'Unknown configuration parameter {k}: '
                                'ignored.')
                    del(k)

        conf = self.default_conf.copy()
        if type(user_conf) is PosixPath:
            # Load user conf as file and update default conf
            config_file = user_conf
            # Load YAML file as dict
            try:
                with open(config_file, 'r') as f:
                    user_conf_dict = yaml.safe_load(f)
            except FileNotFoundError as e:
                log.error(f'''"{e.filename}" file not found.
Consider initializing an nbcourse project with:
nbcourse --init\
''')
                sys.exit()
            sanitize(user_conf_dict)
            update_dict(conf, user_conf_dict)
            conf['project_path'] = config_file.absolute().parent
            conf['config_file'] = config_file
        else:
            if type(user_conf) is dict:
                # Load user conf as dict and update default conf
                sanitize(user_conf)
                update_dict(conf, user_conf)
            else:
                # Only default config is loaded (used for tests only)
                log.debug("Default configuration is used")
            conf['project_path'] = Path.cwd()
            conf['config_file'] = None
        return conf

    def _get_pages(self):
        """get a list of target html pages from markdown source"""
        # Start html_pages list with index.html
        html_pages = [self.conf['output_path'] / self.conf['pages']['home']]
        for path in self.md_page_paths:
            html_pages.append(self.conf['output_path'] /
                              Path(path.name).with_suffix('.html'))
        return html_pages

    def build_pages(self):
        """
        Build a mini website using html templating and markdown conversion
        """

        # List mardkown files
        md_page_paths = list(self.conf['pages']['path'].glob('*.md'))
        # Instanciate all markdown pages to be rendered
        md_pages = [MarkdownPage(self, md_page_path)
                    for md_page_path in md_page_paths]

        def render_children(parent):
            """Recursive function to render children pages from parent page"""
            children = (md_page for md_page in md_pages
                        if md_page.parent_name == parent.name)
            for child in children:
                # Render markdown pages
                child.render(parent)
                render_children(child)

        # First build homepage
        homepage = HomePage(self)
        homepage.render()

        # Then build children pages
        render_children(homepage)

    def build_book(self):
        """Build a pdf book using bookbook"""

        book = Book(self.conf)
        book.build()

    def task_output_dir(self):
        """Create empty output directory"""
        return {
            'targets': [self.conf['output_path']],
            'actions': [(create_folder, [self.conf['output_path']])],
            'uptodate': [self.conf['output_path'].is_dir],
            'clean': True,
        }

    def get_src_dst_paths(self, src_path: Path):
        """Return a tuple of file paths for source and destination"""
        if src_path.is_dir():
            files = get_file_list(src_path)
            src_files = [src_path / file for file in files]
            dst_path = self.conf['output_path'] / Path(src_path.name)
            dst_files = [dst_path / file for file in files]
        else:  # dealing with single file, preserve directory tree
            src_files = [src_path]
            rpath = src_path.relative_to(self.conf['nb']['path'])
            dst_path = self.conf['output_path'] / rpath
            dst_files = [dst_path]
        return src_files, dst_path, dst_files

    def task_copy_material(self):
        """Copy notebook and theme material to output directory"""
        for parent in 'nb', 'theme':
            for src_path in self.conf[parent]['material_paths']:
                src_files, dst_path, dst_files = self.get_src_dst_paths(
                    src_path)
                self.material += dst_files
                yield {
                    'name': dst_path,
                    'file_dep': src_files,
                    'targets': dst_files,
                    'actions': [(update_material, (src_path, dst_path))],
                    'clean': [(clean_tree, (dst_path,))],
                }

    def task_copy_reveal(self):
        """Copy reveal.js to output directory"""
        if self.conf['local_reveal']:
            src_path = self.conf['reveal_path']
            src_files, dst_path, dst_files = self.get_src_dst_paths(src_path)
            return {
                'file_dep': src_files,
                'targets': dst_files,
                'actions': [(update_material, (src_path, dst_path))],
                'clean': [(clean_tree, (dst_path,))],
            }
        else:
            return {
                'uptodate': [True],
                'actions': []
            }

    def execute_notebook(self, notebook: Path, executed_notebook: Path):
        """Execute notebook and write result to executed_notebook file"""
        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=self.conf['nb']['timeout'],
                                 allow_errors=True)
        ep.preprocess(nb, {'metadata': {'path': self.conf['nb']['path']}})

        with open(executed_notebook, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    def _get_executed_nb_path(self, notebook) -> Path:
        """Return executed notebook path"""
        return self.conf['output_path'] / Path(notebook.name)

    def task_execute_notebooks(self):
        """Write executed notebooks to output directory"""
        for notebook in self.notebooks:
            executed_notebook = self._get_executed_nb_path(notebook)
            yield {
                'name': executed_notebook,
                'file_dep': [notebook],
                'task_dep': ['copy_material'],
                'targets': [executed_notebook],
                'clean': True,
                'actions': [(self.execute_notebook, (notebook,
                                                     executed_notebook))],
            }

    def convert_notebook(self, notebook: Path,
                         output_file: Path,
                         to='html'):
        """Convert notebook to output_file"""
        log.debug(f"Converting {notebook} to {output_file}")
        if to == 'slide':
            exporter = self.slide_exporter
        else:
            exporter = self.html_exporter

        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)

        body, resources = exporter.from_notebook_node(nb)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(body)

    def task_convert_to_html(self):
        """Convert executed notebook to html page"""
        for notebook in self.notebooks:
            executed_notebook = self._get_executed_nb_path(notebook)
            html = executed_notebook.with_suffix('.html')
            self.htmls.append(html)
            yield {
                'name': html,
                'file_dep': [executed_notebook],
                'targets': [html],
                'clean': True,
                'actions': [(self.convert_notebook,
                             (executed_notebook, html))],
            }

    def task_convert_to_slides(self):
        """Convert executed notebook to reveal slides"""
        for notebook in self.notebooks:
            executed_notebook = self._get_executed_nb_path(notebook)
            slide = executed_notebook.with_suffix('.slides.html')
            self.slides.append(slide)
            yield {
                'name': slide,
                'file_dep': [executed_notebook],
                'uptodate': [config_changed(str(self.conf['local_reveal']))],
                'targets': [slide],
                'clean': True,
                'actions': [(self.convert_notebook,
                             (executed_notebook, slide, 'slide'))],
            }

    def task_zip_chapters(self):
        """Build zip archives for single chapter downloads"""

        for notebook in self.notebooks:
            zip_file = self._get_executed_nb_path(notebook).with_suffix('.zip')
            paths_to_zip = [notebook]
            for path in self.conf['nb']['material_paths']:
                paths_to_zip += get_file_list(path, relative=False)
            self.chapter_zips.append(zip_file.name)
            yield {
                'name': zip_file,
                'file_dep': paths_to_zip,
                'task_dep': ['copy_material'],
                'targets': [zip_file],
                'clean': True,
                'actions': [(zip_files, (zip_file, paths_to_zip))],
            }

    def task_build_pages(self):
        """Build html pages"""
        deps = self.executed_notebooks + self.md_page_paths + self.theme_files
        if self.conf['config_file']:
            deps.append(self.conf['config_file'])
        return {
            'file_dep': deps,
            'task_dep': ['copy_material'],
            'targets': self.html_pages,
            'clean': True,
            'actions': [self.build_pages],
        }

    def task_build_book(self):
        """Build pdf book"""
        if self.book:
            return {
                'file_dep': self.executed_notebooks + [self.titlepage_path],
                'targets': [self.book],
                'clean': True,
                'actions': [self.build_book],
            }
        else:
            return {
                'uptodate': [True],
                'actions': []
            }

    def task_zip_archive(self):
        """Build a single zip archive for all material"""
        paths_to_zip = self.executed_notebooks + \
            self.html_pages + self.htmls + self.slides + self.material
        if self.book:
            paths_to_zip.append(self.book)
        return {
            'file_dep': paths_to_zip,
            'targets': [self.zip_file],
            'clean': True,
            'actions': [(zip_files, (self.zip_file, paths_to_zip),
                         {'ref_to_arc': (self.conf['output_path'],
                                         self.conf['slug_title'])})],
        }

    def build(self, args: list = None):
        """Build course using Doit"""
        if args is None:
            args = []
        doit_config = {}  # TODO: implement verbosity option
        return MyDoitMain(ClassTaskLoader(self),
                          extra_config=doit_config).run(args)
