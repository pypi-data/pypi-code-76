from yaml.loader import SafeLoader


class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping

def load_yaml_as_document_with_count(entry):
    with open(entry) as file:
        return yaml.load(file,Loader=SafeLineLoader)