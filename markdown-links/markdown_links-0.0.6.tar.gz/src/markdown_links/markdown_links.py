import os
import re
from copy import deepcopy
from pathlib import Path
from re import Pattern
from typing import Optional, List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from uuid import uuid4

from markdown import Markdown
from markdown.extensions import Extension
from markdown.extensions.toc import slugify_unicode
from markdown.inlinepatterns import InlineProcessor, NOIMG
from markdown.treeprocessors import Treeprocessor

_relative_url_pattern: Pattern = re.compile(r'(?!//)([^/][^?#]*)(?:\?([^#]*))?(?:#(.*))?')
_excerpt_depth_attribute = 'data-markdown-links-excerpt-depth'
_excerpt_importance_attribute = 'data-markdown-links-excerpt-importance'


class MarkdownLinks(Extension):
    _inline_pattern = NOIMG + r'\[(.*?)\](\+?)\((.+?)\)(\+?(?:(.+?)\+)?)(?:"(.*?)")?([<>](\d+)?)?'

    def extendMarkdown(self, md: Markdown):
        md.inlinePatterns.register(_InlineProcessor(self._inline_pattern, md), 'markdown_links_inline_processor', 165)
        md.treeprocessors.register(_TreeProcessor(), 'markdown_links_tree_processor', 15)


class _InlineProcessor(InlineProcessor):
    _markdown_title_pattern: Pattern = re.compile(r'^(#+)\s*(\S.*)$')
    _markdown_primer_pattern: Pattern = re.compile(r'^(\w.*?(?:[.!?]|$))')

    def handleMatch(self, m, data):

        href: str = m.group(3)
        is_relative, path, params, anchor = _parse_relative_url(href)

        # filter out non-relative hrefs
        if not is_relative:
            return None, None, None

        # filter out non-markdown-file hrefs
        if not path.endswith('.md') and not path.endswith('.mkd'):  # TODO add more common extensions
            return None, None, None

        document_path: Path = Path() / path

        # filter out non-existent files
        if not document_path.exists():
            return None, None, None

        custom_primer: Optional[str] = m.group(5)
        include_primer: bool = len(m.group(4)) > 0
        include_excerpt: Optional[str] = anchor if m.group(6) == '' else m.group(6)
        composite_title: bool = bool(m.group(2))
        custom_title: Optional[str] = m.group(1)
        document_title: Optional[str] = None
        anchor_title: Optional[str] = None
        primer: Optional[str] = None
        excerpt_lines: List[str] = []
        excerpt_control: Optional[str] = m.group(7)
        excerpt_importance: str = m.group(8) if m.group(8) else '0'

        with document_path.open() as file:

            for line in file:
                title_match = self._markdown_title_pattern.match(line)
                if title_match:
                    title = title_match.group(2)
                    title_level = len(title_match.group(1))
                    if title_level == 1:
                        document_title = title
                    if anchor and anchor.startswith(slugify_unicode(title, '-')):  # TODO get sep from toc conf
                        anchor_title = title
                    if document_title and (anchor_title or not anchor):
                        break

            if include_primer and not custom_primer:
                for line in file:
                    primer_match = self._markdown_primer_pattern.match(line)
                    if primer_match:
                        primer = primer_match.group(1)
                        break

        if include_excerpt:
            with document_path.open() as file:
                for line in file:
                    title_match = self._markdown_title_pattern.match(line)
                    if title_match:
                        title = title_match.group(2)
                        # TODO get sep from toc conf
                        if include_excerpt == title or include_excerpt.startswith(slugify_unicode(title, '-')):
                            include_excerpt = title  # make sure include_excerpt holds the pretty/non-slug title
                            for excerpt_line in file:
                                title_match = self._markdown_title_pattern.match(excerpt_line)
                                if title_match:
                                    break
                                excerpt_lines.append(excerpt_line)

        result = Element('markdown_links_container')

        anchor = Element('a')
        anchor.attrib['class'] = 'markdown_links'
        anchor.attrib['href'] = href
        result.append(anchor)
        if composite_title and (custom_title or anchor_title) and document_title:
            anchor.text = (custom_title or anchor_title) + ' '
            span = Element('span')
            span.text = f'({document_title})'
            anchor.append(span)
        else:
            anchor.text = custom_title or anchor_title or document_title or document_path.name

        if include_primer:
            primer = custom_primer or primer
            if primer:
                span = Element('span')
                span.text = ': ' + primer
                result.append(span)
                # TODO maybe turn this into a label for list item excerpts

        if excerpt_lines:

            excerpt_parent = result

            if excerpt_control:
                if excerpt_control.startswith('<'):
                    uuid = str(uuid4())
                    checkbox = Element('input')
                    checkbox.attrib['id'] = uuid
                    checkbox.attrib['class'] = 'markdown_links hidden'
                    checkbox.attrib['type'] = 'checkbox'
                    _initialize_depth_and_importance(checkbox, excerpt_importance, 'checked')
                    result.append(checkbox)
                    label = Element('label')
                    label.attrib['class'] = 'markdown_links'
                    label.attrib['for'] = uuid
                    result.insert(0, label)
                else:
                    details = Element('details')
                    details.attrib['class'] = 'markdown_links'
                    _initialize_depth_and_importance(details, excerpt_importance, 'open')
                    result.append(details)
                    summary = Element('summary')
                    summary.text = include_excerpt + ' from '
                    anchor = Element('a')
                    anchor.attrib['href'] = href
                    anchor.text = document_title or document_path.name
                    summary.append(anchor)
                    details.append(summary)
                    excerpt_parent = details

            return_dir = os.getcwd()
            os.chdir(document_path.parent)

            md = deepcopy(self.md)
            md.stripTopLevelTags = False
            excerpt = ElementTree.fromstring(md.convert(''.join(excerpt_lines)))
            if len(excerpt) == 1:
                excerpt = excerpt[0]
            excerpt.attrib['class'] = 'markdown_links_excerpt'

            for element in _recurse(excerpt):
                _fix_attribute_relative_url(element, 'href', return_dir)
                _fix_attribute_relative_url(element, 'src', return_dir)
                excerpt_depth = int(element.attrib.get(_excerpt_depth_attribute, -1))
                if excerpt_depth > -1:
                    excerpt_depth += 1
                    element.attrib[_excerpt_depth_attribute] = str(excerpt_depth)
                    importance = int(element.attrib.get(_excerpt_importance_attribute, 0))
                    attribute = 'checked' if element.tag == 'input' else 'open'
                    if importance > excerpt_depth:
                        element.attrib[attribute] = attribute
                    else:
                        element.attrib.pop(attribute, None)
            excerpt_parent.append(excerpt)

            os.chdir(return_dir)

        return result, m.start(0), m.end(0)


class _TreeProcessor(Treeprocessor):

    def run(self, root: ElementTree):
        for grand_parent, j, parent in _recurse_with_parent_index(root):
            i = 0
            while i < len(parent):
                child = parent[i]
                if child.tag == 'markdown_links_container':
                    del parent[i]
                    for transfer_child in child:
                        if parent.tag != 'p' or transfer_child.tag in ('a', 'span'):
                            parent.insert(i, transfer_child)
                            i += 1
                        else:
                            j += 1
                            while j < len(grand_parent) and \
                                    grand_parent[j].get('class', None) == 'markdown_links_excerpt':
                                j += 1
                            grand_parent.insert(j, transfer_child)
                    parent[i - 1].tail = child.tail
                else:
                    i += 1


def _parse_relative_url(link: str):
    match = _relative_url_pattern.match(link)
    if not match:
        return False, None, None, None
    return True, match.group(1), match.group(2), match.group(3)


def _recurse(element_tree: ElementTree):
    yield element_tree
    for child in element_tree:
        yield from _recurse(child)


def _recurse_with_parent_index(element_tree: ElementTree, parent: ElementTree = None, index: int = 0):
    if parent:
        yield parent, index, element_tree
    i = 0
    while i < len(element_tree):
        yield from _recurse_with_parent_index(element_tree[i], element_tree, i)
        i += 1


def _initialize_depth_and_importance(element: Element, importance: str, attribute: str):
    element.attrib[_excerpt_depth_attribute] = '0'
    if importance != '0':
        element.attrib[_excerpt_importance_attribute] = importance
        element.attrib[attribute] = attribute


def _fix_attribute_relative_url(element: Element, attribute: str, anchor_path):
    value = element.attrib.get(attribute, None)
    if value:
        is_relative, path, params, anchor = _parse_relative_url(value)
        if is_relative:
            element.attrib[attribute] = os.path.relpath(path, anchor_path)
            if params:
                element.attrib[attribute] += '?' + params
            if anchor:
                element.attrib[attribute] += '#' + anchor


def makeExtension(**kwargs):
    return MarkdownLinks(**kwargs)
