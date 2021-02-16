from . import log
import nbformat
import re
import markdown
from pathlib import Path
from pprint import pformat
import jinja2
from bs4 import BeautifulSoup
import frontmatter
import sys


class Page:
    """An abstract class for a static web page"""

    html_template = ''
    html = ''

    def __init__(self, nbcourse):
        conf = nbcourse.conf.copy()
        self.html_path = conf['output_path'] / self.html
        self.title = conf['title']
        self.template_path = conf['template_path']
        self.variables = conf
        self.notebooks = nbcourse.notebooks

    def _render_template(self):
        """Return html rendered from template and variables"""

        # Inject variables into html_template
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                 self.template_path.as_posix()))
        template = env.get_template(self.html_template)
        html_out = template.render(self.variables)
        with open(self.html_path, 'w') as f:
            f.write(html_out)

    def render(self):
        """Render html using templating"""
        raise NotImplementedError()


class HomePage(Page):
    """A class to handle a homepage to be rendered"""

    html_template = "index.html.j2"
    html = "index.html"
    name = 'home'
    parent = None
    parent_name = ''

    def __init__(self, nbcourse):
        super().__init__(nbcourse)
        self.chapters = {}

    @staticmethod
    def _get_chapter(path: Path):
        """Get chapter from notebook file (source: bookbook)"""

        chapter_no = int(re.match(r'(\d+)\-', path.stem).group(1))
        nb = nbformat.read(str(path), as_version=4)

        if nb.cells[0].cell_type != 'markdown':
            log.error(f"The first cell of the notebook {path} should be Markdown type " +
                      f"({nb.cells[0].cell_type} instead).")
            sys.exit()
        lines = nb.cells[0].source.splitlines()
        if lines[0].startswith('# '):
            header = lines[0][2:]
        elif len(lines) > 1 and lines[1].startswith('==='):
            header = lines[0]
        else:
            log.error(f"No heading found in {path}")
            sys.exit()

        assert path.suffix == '.ipynb', path

        return {'number': chapter_no,
                'title': header,
                'filename': path.stem}

    def _get_variables(self):
        """Set some variables from conf dictionnary and notebooks files"""

        def build_link_name(link_type: str, suffix: str):
            """Build archive or pdf book links from slug name"""
            if link_type in self.variables['links']:
                try:
                    # For example look for yaml entry: `book: file: filename.pdf`
                    self.variables['links'][link_type]['target'] = \
                        self.variables[link_type]['file']
                except KeyError:
                    # Use <slug_title>.pdf
                    self.variables['links'][link_type]['target'] = \
                        self.variables['slug_title'] + suffix

        # Get chapters from notebook files
        chapters = []
        for nbfile in self.notebooks:
            chapter = self._get_chapter(nbfile)
            try:
                chapter['preview_only'] = chapter['number'] in \
                    self.variables['chapter_preview_only']
            except KeyError:
                chapter['preview_only'] = False
            chapters.append(chapter)
        chapters.sort(key=lambda chapter: chapter['number'])
        self.variables.update({'chapters': chapters})
        build_link_name('book', '.pdf')
        build_link_name('archive', '.zip')

        log.debug("Homepage template variables:")
        log.debug(pformat(self.variables))

    def _render_template(self):
        """Return html rendered from template and variables"""

        # Inject variables into html_template
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                 self.template_path.as_posix()))
        template = env.get_template(self.html_template)
        html_out = template.render(self.variables)
        with open(self.html_path, 'w') as f:
            f.write(html_out)

    def render(self):
        """Render html using templating"""
        self._get_variables()
        self._render_template()


class MarkdownPage(Page):

    html_template = "page.html.j2"

    def __init__(self, nbcourse, src: Path):
        super().__init__(nbcourse)
        self.src = src
        self.html = Path(self.src.name).with_suffix('.html')
        self.html_path = nbcourse.conf['output_path'] / self.html

        with open(self.src, 'r') as md_file:
            metadata, self.md_content = frontmatter.parse(md_file.read())
        self.title = metadata['title']
        self.parent_name = metadata.get('parent', 'home')
        self.name = self.src.name
        self.parent = None  # to be populate later

    def get_menu_list(self):
        """Return a list to be displayed as a top menu"""
        # At least current page
        menu = [(self.title, self.html)]
        page = self  # Initialize with current page
        # Ascend to parent page
        while page.parent.parent:
            menu.append((page.parent.title, page.parent.html))
            page = page.parent
        menu.reverse()
        return menu

    def render(self, parent):
        """Render markdown file into html file adding ToC"""

        self.parent = parent
        pattern = re.compile(r'^pages\/(.*)\.md$')

        def markdown2html():
            """Return html from markdown file"""
            md = markdown.Markdown(extensions=['fenced_code', 'codehilite',
                                               'toc'])
            body = md.convert(self.md_content)

            # Transform link to file.md into link to file.html
            soup = BeautifulSoup(body, 'html.parser')
            for link in soup.findAll(['a']):
                href = link.get('href')
                link['href'] = pattern.sub(r'\1.html', href)

            return soup.prettify(), md.toc

        body, toc = markdown2html()
        self.variables = {'title': self.title,
                          'article_content': body,
                          'toc': toc,
                          'menu': self.get_menu_list()}
        self._render_template()
