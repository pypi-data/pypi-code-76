# This recursively expands the templates specified in the XML source file,
# and writes the result to an HTML file. During the expansion, templates
# have access to both the project variables and the attributes and content
# provided with the corresponding tag.
import os.path
from lxml import etree as ET
from salal.core.log import log
from salal.core.config import config
from salal.core.utilities import utilities

class SVGHandler:

    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['svg']

    #---------------------------------------------------------------------------

    @classmethod
    def check_for_def_uses_in_elements(cls, root, attribute, prefix, f_trim, b_trim, def_uses):
        elements = root.findall('.//*[@' + attribute + ']')
        for element in elements:
            if element.attrib[attribute].find(prefix) != -1:
                if b_trim:
                    used_def = element.attrib[attribute][f_trim:b_trim]
                else:
                    used_def = element.attrib[attribute][f_trim:]
                if used_def in def_uses:
                    def_uses[used_def] += 1

    #---------------------------------------------------------------------------

    @classmethod
    def check_for_def_uses_in_styles(cls, root, attribute, f_trim, b_trim, def_uses):
        for element in root.findall('./{*}style[@type="text/css"]'):
            for line in element.text.split('\n'): 
                if line.count(attribute):
                    used_def = line.strip().split()[1][f_trim:b_trim]
                    if used_def in def_uses:
                        def_uses[used_def] += 1

    #---------------------------------------------------------------------------

    @classmethod
    def remove_unused_defs (cls, svg_root):
        def_elements = dict()
        def_uses = dict()
        for element in svg_root.iterfind('./{*}defs/*[@id]'):
            def_elements[element.attrib['id']] = element
            def_uses[element.attrib['id']] = 0
        cls.check_for_def_uses_in_elements(svg_root, 'stroke', 'url(#', 5, -1, def_uses)
        cls.check_for_def_uses_in_elements(svg_root, 'fill', 'url(#', 5, -1, def_uses)
        cls.check_for_def_uses_in_elements(svg_root, 'href', '#', 1, None, def_uses)
        cls.check_for_def_uses_in_styles(svg_root, 'stroke', 5, -2, def_uses)
        cls.check_for_def_uses_in_styles(svg_root, 'fill', 5, -2, def_uses)
        for id in def_uses:
            if def_uses[id] == 0:
                parent = def_elements[id].getparent()
                parent.remove(def_elements[id])

    #---------------------------------------------------------------------------
    # This is a fairly fragile function - it depends on there only being
    # one stylesheet, and it being a specific site-wide css file with a
    # particular name and location on the server. It also uses a hack
    # in lxml to remove the old stylesheet and add a new one.

    @classmethod
    def make_server_ready_stylesheet (cls, svg_root):
        els = svg_root.xpath("preceding-sibling::node()")
        for el in els:
            if hasattr(el, 'target') and (el.target == 'xml-stylesheet'):
                new_el = ET.ProcessingInstruction('xml-stylesheet', 'type="text/css" href="{{ SITE_ROOT }}/css/svg-style.css"')
                svg_root.addprevious(new_el)
                # This weird code is because there is no direct way to remove
                # a processing instruction from the tree. What this code does
                # it moves it from being a sibling of the svg node to a child,
                # at which point it can be removed.
                svg_root.append(el)
                svg_root.remove(el)

    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):

        log.message('TRACE', 'Preparing SVG file')
        tree = ET.parse(os.path.join(source_dir, file_stem + '.' + tag))
        root = tree.getroot()
        cls.remove_unused_defs(root)
        cls.make_server_ready_stylesheet(root)
        tree_string = ET.tostring(tree, pretty_print=True, xml_declaration=True, method="xml").decode()
        output = utilities.substitute_variables(tree_string, config.project)
        with open(os.path.join(target_dir, file_stem + '.' + tag), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(output)
            
    #---------------------------------------------------------------------------

handler = SVGHandler
