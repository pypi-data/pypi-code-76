import importlib
import pkgutil
from dentmark.defs_manager import DefsManager
from dentmark.parser import Parser

class Dentmark:
    def __init__(self, defs_module_name=None):
        self.defs_module_name = defs_module_name
        self.available_definitions = self._find_defs()

        if defs_module_name:
            if defs_module_name not in self.available_definitions:
                raise Exception(f'No definitions module named: {defs_module_name}')
            else:
                registered_tags = self.available_definitions[defs_module_name].REGISTERED_TAGS
        else:
            from dentmark.default_definitions import REGISTERED_TAGS
            registered_tags = REGISTERED_TAGS

        self.defs_manager = DefsManager(registered_tags)

    def _find_defs(self):
        return {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith('dentmark_')
        }


    def parse(self, file_name_or_str):
        p = Parser(self.defs_manager, file_name_or_str)
        return p.parse()


    def render(self, file_name_or_str, extra_context={}):
        root = self.parse(file_name_or_str)
        root.pre_render(root, extra_context)
        rendered = root.render()
        return rendered


    def add_element(self, file_name_or_str, tag_id, new_tag_name, value):
        root = self.parse(file_name_or_str)
        found_element = root.get_tag_by_id(tag_id)
        if found_element is None:
            raise Exception('Element for tag_id not found: {tag_id}')
        found_element.add_child_element(self.defs_manager, new_tag_name, value)
        return root
