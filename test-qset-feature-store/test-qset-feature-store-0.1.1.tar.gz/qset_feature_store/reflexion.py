from utils_ak.interactive_imports import *
import qset_feature_store

import re


def get_featureset_code_from_current_notebook(featureset):
    code = get_current_notebook_code()
    cells = parse_cells(code)

    featureset_class_name = re.search(r"'(.+)'", str(featureset)).groups()[0].split('.')[-1]
    cell = [cell for cell in cells if f'class {featureset_class_name}(' in cell][0]
    cell = re.sub(r'\n+', '\n', cell)
    cell = re.sub(r'^\n', '', cell)
    cell = re.sub(r'\n$', '', cell)
    return cell


def _is_featureset_child(obj):
    if not inspect.isclass(obj):
        return False

    if obj == qset_feature_store.FeatureSet:
        return False

    if not any(['FeatureSet' in str(base) for base in obj.__mro__]):
        return False

    try:
        return isinstance(obj(), qset_feature_store.FeatureSet)
    except:
        return False


def extract_feature_set(code):
    with tempfile(suffix='.py') as fn:

        with open(fn, 'w') as f:
            f.write(code)

        classes = extract_all_classes(fn)
        classes = {k: v for k, v in classes.items() if _is_featureset_child(classes[k])}
        assert len(classes) == 1
        key = list(classes.keys())[0]
        return classes[key]
